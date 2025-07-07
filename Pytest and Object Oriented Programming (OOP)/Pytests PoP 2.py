import os
import tempfile
import random
import pytest

from chess import (
    location2index, index2location, split_move,
    is_piece_at, piece_at,
    Bishop, King,
    is_check, is_checkmate, is_stalemate,
    read_board, save_board,
    conf2unicode, find_black_move
)

# 5 tests for location2index

def test_location2index_A1():
    assert location2index("A1") == (1, 1)

def test_location2index_b2():
    assert location2index("b2") == (2, 2)

def test_location2index_Z26():
    assert location2index("Z26") == (26, 26)

def test_location2index_M10():
    assert location2index("m10") == (13, 10)

def test_location2index_invalid():
    with pytest.raises(ValueError):
        location2index("1A")

# 5 tests for index2location

def test_index2location_1_1():
    assert index2location(1, 1) == "A1"

def test_index2location_2_3():
    assert index2location(2, 3) == "B3"

def test_index2location_26_26():
    assert index2location(26, 26) == "Z26"

def test_index2location_5_10():
    assert index2location(5, 10) == "E10"

def test_index2location_13_1():
    assert index2location(13, 1) == "M1"

# 5 tests for split_move

def test_split_move_simple():
    assert split_move("A1B2") == ("A1", "B2")

def test_split_move_lower():
    assert split_move("e2e4") == ("e2", "e4")

def test_split_move_long():
    assert split_move("A10B20") == ("A10", "B20")

def test_split_move_mixed():
    assert split_move("m10z5") == ("m10", "z5")

def test_split_move_diagonal():
    assert split_move("H8A1") == ("H8", "A1")

# 5 tests for is_piece_at

def test_is_piece_at_present():
    B = (3, [Bishop(1,1,True), King(3,3,False)])
    assert is_piece_at(1, 1, B)

def test_is_piece_at_absent():
    B = (3, [Bishop(1,1,True)])
    assert not is_piece_at(2, 2, B)

def test_is_piece_at_edge():
    B = (3, [King(3,3,False)])
    assert is_piece_at(3, 3, B)

def test_is_piece_at_false_edge():
    B = (3, [King(3,3,False)])
    assert not is_piece_at(1, 3, B)

def test_is_piece_at_empty_board():
    B = (3, [])
    assert not is_piece_at(2, 2, B)

# 5 tests for piece_at

def test_piece_at_single():
    bishop = Bishop(1,1,True)
    B = (3, [bishop])
    assert piece_at(1, 1, B) is bishop

def test_piece_at_multiple():
    k = King(2,2,False)
    B = (3, [Bishop(1,1,True), k])
    assert piece_at(2, 2, B) is k

def test_piece_at_first():
    b1 = Bishop(1,1,True)
    b2 = Bishop(2,2,True)
    B = (3, [b1, b2])
    assert piece_at(1, 1, B) is b1

def test_piece_at_last():
    b1 = Bishop(1,1,True)
    b2 = Bishop(2,2,True)
    B = (3, [b1, b2])
    assert piece_at(2, 2, B) is b2

def test_piece_at_missing_raises():
    with pytest.raises(Exception):
        piece_at(3, 3, (3, [Bishop(1,1,True)]))

# 5 tests for Bishop.can_reach

def test_bishop_can_reach_clear():
    b = Bishop(1,1,True)
    B = (3, [b])
    assert b.can_reach(2,2,B)

def test_bishop_can_reach_blocked():
    b = Bishop(1,1,True)
    blocker = Bishop(2,2,True)
    B = (3, [b, blocker])
    assert not b.can_reach(3,3,B)

def test_bishop_can_reach_not_diagonal():
    b = Bishop(1,1,True)
    B = (3, [b])
    assert not b.can_reach(1,2,B)

def test_bishop_can_reach_out_of_bounds():
    b = Bishop(1,1,True)
    B = (3, [b])
    assert not b.can_reach(4,4,B)

def test_bishop_can_reach_capture_enemy():
    b = Bishop(1,1,True)
    enemy = King(3,3,False)
    B = (3, [b, enemy])
    assert b.can_reach(3,3,B)

# 5 tests for Bishop.can_move_to

def test_bishop_can_move_to_empty():
    b = Bishop(1,1,True)
    B = (3, [b])
    assert b.can_move_to(2,2,B)

def test_bishop_can_move_to_capture_enemy():
    b = Bishop(1,1,True)
    enemy = King(2,2,False)
    B = (3, [b, enemy])
    assert b.can_move_to(2,2,B)

def test_bishop_can_move_to_blocked_by_same():
    b = Bishop(1,1,True)
    friend = Bishop(2,2,True)
    B = (3, [b, friend])
    assert not b.can_move_to(2,2,B)

def test_bishop_can_move_to_illegal():
    b = Bishop(1,1,True)
    B = (3, [b])
    assert not b.can_move_to(1,2,B)

def test_bishop_can_move_to_leaves_king_safe(monkeypatch):
    b = Bishop(1,1,True)
    monkeypatch.setattr('chess.is_check', lambda side, board: True)
    B = (3, [b])
    assert not b.can_move_to(2,2,B)

# 5 tests for Bishop.move_to

def test_bishop_move_to_valid():
    b = Bishop(1,1,True)
    B = (3, [b])
    newB = b.move_to(2,2,B)
    assert is_piece_at(2,2,newB)

def test_bishop_move_to_capture():
    b = Bishop(1,1,True)
    enemy = King(2,2,False)
    B = (3, [b, enemy])
    newB = b.move_to(2,2,B)
    assert is_piece_at(2,2,newB) and not is_piece_at(1,1,newB)

def test_bishop_move_to_invalid_raises():
    b = Bishop(1,1,True)
    B = (3, [b])
    with pytest.raises(ValueError):
        b.move_to(3,3,B)

def test_bishop_move_to_no_side_conflict():
    b = Bishop(1,1,True)
    B = (3, [b])
    newB = b.move_to(2,2,B)
    assert isinstance(newB[1][-1], Bishop)

def test_bishop_move_to_board_size_unchanged():
    b = Bishop(1,1,True)
    B = (5, [b])
    newB = b.move_to(2,2,B)
    assert newB[0] == 5

# 5 tests for Bishop.__str__

def test_bishop_str_single():
    b = Bishop(1,1,True)
    B = (3, [b])
    assert b.__str__(B) == "Wb1"

def test_bishop_str_multiple():
    b1 = Bishop(1,1,True)
    b2 = Bishop(2,1,True)
    B = (3, [b1, b2])
    assert b2.__str__(B) == "Wb2"

def test_bishop_str_black():
    b = Bishop(1,1,False)
    B = (3, [b])
    assert b.__str__(B) == "Bb1"

def test_bishop_str_order():
    b1 = Bishop(1,1,True)
    b2 = Bishop(1,2,True)
    b3 = Bishop(2,1,True)
    B = (3, [b3, b1, b2])
    assert b2.__str__(B) == "Wb3"

def test_bishop_str_consistent():
    b = Bishop(1,1,True)
    B1 = (3, [b])
    B2 = (3, [b, Bishop(2,2,True)])
    assert b.__str__(B1) != b.__str__(B2)

# 5 tests for King.can_reach

def test_king_can_reach_one_step():
    k = King(2,2,True)
    B = (5, [k])
    assert k.can_reach(3,3,B)

def test_king_can_reach_too_far():
    k = King(2,2,True)
    B = (5, [k])
    assert not k.can_reach(4,4,B)

def test_king_can_reach_blocked_same():
    k = King(2,2,True)
    friend = Bishop(3,3,True)
    B = (5, [k, friend])
    assert not k.can_reach(3,3,B)

def test_king_can_reach_capture_enemy():
    k = King(2,2,True)
    enemy = Bishop(3,2,False)
    B = (5, [k, enemy])
    assert k.can_reach(3,2,B)

def test_king_can_reach_zero_move():
    k = King(2,2,True)
    B = (5, [k])
    assert k.can_reach(2,2,B)

# 5 tests for King.can_move_to

def test_king_can_move_to_valid_capture():
    k = King(1,1,True)
    enemy = Bishop(2,2,False)
    B = (5, [k, enemy])
    assert k.can_move_to(2,2,B)

def test_king_can_move_to_out_of_bounds_raises():
    k = King(1,1,True)
    B = (5, [k])
    with pytest.raises(ValueError):
        k.can_move_to(0,0,B)

def test_king_can_move_to_blocked_same():
    k = King(1,1,True)
    friend = Bishop(2,2,True)
    B = (5, [k, friend])
    assert not k.can_move_to(2,2,B)

def test_king_can_move_to_leaves_in_check(monkeypatch):
    k = King(1,1,True)
    monkeypatch.setattr('chess.is_check', lambda side, board: True)
    B = (5, [k])
    assert not k.can_move_to(2,1,B)

def test_king_can_move_to_no_piece():
    k = King(1,1,True)
    B = (5, [k])
    assert k.can_move_to(2,1,B)

# 5 tests for King.move_to

def test_king_move_to_valid():
    k = King(1,1,True)
    B = (5, [k])
    newB = k.move_to(2,2,B)
    assert is_piece_at(2,2,newB)

def test_king_move_to_invalid_raises():
    k = King(1,1,True)
    B = (5, [k])
    with pytest.raises(ValueError):
        k.move_to(3,3,B)

def test_king_move_to_capture():
    k = King(1,1,True)
    enemy = Bishop(2,1,False)
    B = (5, [k, enemy])
    newB = k.move_to(2,1,B)
    assert is_piece_at(2,1,newB) and not is_piece_at(1,1,newB)

def test_king_move_to_no_side_conflict():
    k = King(1,1,True)
    B = (5, [k])
    newB = k.move_to(2,2,B)
    assert any(isinstance(p, King) for p in newB[1])

def test_king_move_to_board_size_preserved():
    k = King(1,1,True)
    B = (7, [k])
    newB = k.move_to(2,1,B)
    assert newB[0] == 7

# 5 tests for King.__str__

def test_king_str_white():
    k = King(1,1,True)
    B = (3, [k])
    assert k.__str__(B) == "Wk1"

def test_king_str_black():
    k = King(1,1,False)
    B = (3, [k])
    assert k.__str__(B) == "Bk1"

def test_king_str_multiple():
    k1 = King(1,1,True)
    k2 = King(2,2,True)
    B = (4, [k1, k2])
    assert k2.__str__(B) == "Wk2"

def test_king_str_ordering():
    k1 = King(2,2,True)
    k2 = King(1,1,True)
    B = (4, [k1, k2])
    assert k2.__str__(B) == "Wk2"

def test_king_str_changes():
    k = King(1,1,True)
    B1 = (3, [k])
    B2 = (3, [k, King(2,2,True)])
    assert k.__str__(B1) != k.__str__(B2)

# 5 tests for is_check

def test_is_check_true():
    king = King(2,2,True)
    enemy = Bishop(1,1,False)
    B = (4, [king, enemy])
    assert is_check(True, B)

def test_is_check_false_no_attack():
    king = King(2,2,True)
    B = (4, [king])
    assert not is_check(True, B)

def test_is_check_false_wrong_side():
    king = King(2,2,True)
    enemy = Bishop(1,1,True)
    B = (4, [king, enemy])
    assert not is_check(True, B)

def test_is_check_enemy_attacks_from_distance():
    king = King(3,3,True)
    enemy = Bishop(1,1,False)
    B = (4, [king, enemy])
    assert is_check(True, B)

def test_is_check_multiple_attackers():
    king = King(3,3,True)
    e1 = Bishop(2,2,False)
    e2 = Bishop(1,5,False)
    B = (6, [king, e1, e2])
    assert is_check(True, B)

# 5 tests for is_checkmate

def test_is_checkmate_true_simple():
    kb = King(1,1,False)
    wb1 = Bishop(2,3,True)
    wb2 = Bishop(3,2,True)
    B = (4, [kb, wb1, wb2])
    assert is_checkmate(False, B)

def test_is_checkmate_false_not_in_check():
    kb = King(1,1,False)
    B = (4, [kb])
    assert not is_checkmate(False, B)

def test_is_checkmate_false_has_escape():
    kb = King(2,2,False)
    wb = Bishop(1,3,True)
    B = (4, [kb, wb])
    assert not is_checkmate(False, B)

def test_is_checkmate_full_block():
    kb = King(1,1,False)
    blockers = [Bishop(2,1,True), Bishop(1,2,True), Bishop(2,2,True)]
    B = (3, [kb] + blockers)
    assert is_checkmate(False, B)

def test_is_checkmate_multiple_pieces():
    kb = King(1,1,False)
    wb1 = Bishop(2,3,True)
    wb2 = Bishop(3,2,True)
    extra = Bishop(4,4,True)
    B = (5, [kb, wb1, wb2, extra])
    assert is_checkmate(False, B)

# 5 tests for is_stalemate

def test_is_stalemate_true_simple():
    kb = King(1,1,False)
    wb1 = Bishop(2,2,True)
    wb2 = Bishop(3,1,True)
    B = (4, [kb, wb1, wb2])
    assert is_stalemate(False, B)

def test_is_stalemate_false_in_check():
    kb = King(2,2,False)
    wb = Bishop(1,1,True)
    B = (4, [kb, wb])
    assert not is_stalemate(False, B)

def test_is_stalemate_false_has_move():
    kb = King(2,2,False)
    wb = Bishop(1,5,True)
    B = (6, [kb, wb])
    assert not is_stalemate(False, B)

def test_is_stalemate_large_board():
    kb = King(1,1,False)
    B = (8, [kb])
    assert not is_stalemate(False, B)

def test_is_stalemate_other_side():
    kb_w = King(1,1,True)
    B = (4, [kb_w])
    assert not is_stalemate(True, B)

# 5 tests for read_board and save_board

def test_read_board_valid(tmp_path):
    content = """
3
B A1, K B2
K C3
"""
    f = tmp_path / "b.txt"
    f.write_text(content)
    B = read_board(str(f))
    assert B[0] == 3

def test_read_board_missing_lines(tmp_path):
    f = tmp_path / "b2.txt"
    f.write_text("3\nB A1")
    with pytest.raises(IOError):
        read_board(str(f))

def test_read_board_invalid_piece(tmp_path):
    f = tmp_path / "b3.txt"
    f.write_text("3\nX A1\nK B2")
    with pytest.raises(IOError):
        read_board(str(f))

def test_save_board_roundtrip(tmp_path):
    b = Bishop(1,1,True)
    k = King(2,2,False)
    B = (4, [b, k])
    out = tmp_path / "out.txt"
    save_board(str(out), B)
    text = out.read_text()
    assert "4" in text

def test_read_save_extra_whitespace(tmp_path):
    content = """
5
  B A1 ,K B2  

"""
    f = tmp_path / "b4.txt"
    f.write_text(content)
    B = read_board(str(f))
    out = tmp_path / "o4.txt"
    save_board(str(out), B)
    assert "5" in out.read_text()

# 5 tests for conf2unicode

def test_conf2unicode_empty():
    B = (2, [])
    u = conf2unicode(B)
    assert " " in u

def test_conf2unicode_bishop_king():
    b = Bishop(1,2,False)
    k = King(2,1,True)
    B = (2, [b, k])
    u = conf2unicode(B)
    assert "♝" in u and "♔" in u

def test_conf2unicode_size():
    B = (3, [])
    u = conf2unicode(B)
    assert len(u.splitlines()) == 3

def test_conf2unicode_positions():
    b = Bishop(3,1,False)
    B = (3, [b])
    rows = conf2unicode(B).splitlines()
    # bishop on bottom row = last line
    assert "♝" in rows[-3]

def test_conf2unicode_no_duplicates():
    b1 = Bishop(1,1,True)
    b2 = Bishop(1,1,False)
    B = (2, [b1, b2])
    u = conf2unicode(B)
    # only one piece per square representation
    assert u.count("♗") <= 1

# 5 tests for find_black_move

def test_find_black_move_single(monkeypatch):
    bb = Bishop(1,1,False)
    B = (3, [bb])
    monkeypatch.setattr(random, 'shuffle', lambda x: x)
    piece,x,y = find_black_move(B)
    assert piece is bb and (x,y) != (None,None)

def test_find_black_move_multiple(monkeypatch):
    bb1 = Bishop(1,1,False)
    bb2 = Bishop(2,2,False)
    B = (3, [bb1, bb2])
    piece,x,y = find_black_move(B)
    assert piece in (bb1, bb2)

def test_find_black_move_returns_ints():
    bb = Bishop(1,1,False)
    B = (4, [bb])
    piece,x,y = find_black_move(B)
    assert isinstance(x, int) and isinstance(y, int)

def test_find_black_move_no_white():
    bb = Bishop(1,1,False)
    B = (2, [bb])
    piece,x,y = find_black_move(B)
    assert piece.side_ is False

def test_find_black_move_some_move_possible():
    bb = Bishop(1,1,False)
    B = (3, [bb])
    piece,x,y = find_black_move(B)
    # bishop from (1,1) can only move diagonally
    assert x != 1 or y != 1
