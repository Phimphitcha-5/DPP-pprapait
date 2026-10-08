import pygame
from checkmate import checkmate

pygame.init()

WIDTH = 760
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CHECKMATE - Blue & White")

# ---------- Colors ----------
BACKGROUND = (225, 242, 255)
WHITE_SQUARE = (248, 252, 255)
BLUE_SQUARE = (135, 200, 235)
DARK_BLUE = (40, 115, 175)
DEEP_BLUE = (25, 75, 120)
SELECT_BLUE = (70, 170, 245)
MOVE_BLUE = (175, 225, 255)
RED = (235, 80, 95)
BLACK_PIECE = (35, 65, 90)
WHITE_PIECE = (180, 225, 250)
WHITE_PIECE_OUTLINE = (90, 165, 215)
BLACK_PIECE_OUTLINE = (210, 235, 250)
SHADOW = (170, 205, 225)

# ---------- Board ----------
SIZE = 80
BOARD_X = 60
BOARD_Y = 125
BOARD_SIZE = SIZE * 8

# Standard chess starting position.
# Uppercase = White, lowercase = Black.
START_BOARD = [
    list("rnbqkbnr"),
    list("pppppppp"),
    list("........"),
    list("........"),
    list("........"),
    list("........"),
    list("PPPPPPPP"),
    list("RNBQKBNR"),
]

font_title = pygame.font.Font(None, 54)
font_piece = pygame.font.Font(None, 58)
font_small = pygame.font.Font(None, 28)
font_gameover = pygame.font.Font(None, 64)


def board_string(board):
    return "\n".join("".join(row) for row in board)


def inside(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def same_side(piece_a, piece_b):
    if piece_a == "." or piece_b == ".":
        return False
    return piece_a.isupper() == piece_b.isupper()


def enemy(piece_a, piece_b):
    return (
        piece_b != "."
        and piece_a.isupper() != piece_b.isupper()
    )


def find_king(board, white=True):
    king = "K" if white else "k"

    for r in range(8):
        for c in range(8):
            if board[r][c] == king:
                return r, c

    return None


def square_attacked(board, row, col, by_white):
    """
    True when the requested square is attacked by the given side.
    Used for check detection.
    """
    for r in range(8):
        for c in range(8):
            piece = board[r][c]

            if piece == ".":
                continue

            if piece.isupper() != by_white:
                continue

            dr = row - r
            dc = col - c

            if piece.upper() == "P":
                direction = -1 if by_white else 1
                if dr == direction and abs(dc) == 1:
                    return True

            elif piece.upper() == "N":
                if (abs(dr), abs(dc)) in ((1, 2), (2, 1)):
                    return True

            elif piece.upper() == "B":
                if abs(dr) == abs(dc) and path_clear(
                    board, r, c, row, col
                ):
                    return True

            elif piece.upper() == "R":
                if (dr == 0 or dc == 0) and path_clear(
                    board, r, c, row, col
                ):
                    return True

            elif piece.upper() == "Q":
                straight = dr == 0 or dc == 0
                diagonal = abs(dr) == abs(dc)

                if (straight or diagonal) and path_clear(
                    board, r, c, row, col
                ):
                    return True

            elif piece.upper() == "K":
                if max(abs(dr), abs(dc)) == 1:
                    return True

    return False


def path_clear(board, r1, c1, r2, c2):
    dr = (r2 > r1) - (r2 < r1)
    dc = (c2 > c1) - (c2 < c1)

    r, c = r1 + dr, c1 + dc

    while (r, c) != (r2, c2):
        if board[r][c] != ".":
            return False

        r += dr
        c += dc

    return True


def is_in_check(board, white):
    king = find_king(board, white)

    if king is None:
        return False

    return square_attacked(
        board,
        king[0],
        king[1],
        not white
    )


def pseudo_moves(board, row, col):
    """Generate movement squares without ignoring check."""
    piece = board[row][col]

    if piece == ".":
        return []

    white = piece.isupper()
    kind = piece.upper()
    moves = []

    if kind == "P":
        direction = -1 if white else 1
        start_row = 6 if white else 1

        # Forward one square.
        nr = row + direction

        if inside(nr, col) and board[nr][col] == ".":
            moves.append((nr, col))

            # Forward two squares from starting position.
            nr2 = row + 2 * direction

            if (
                row == start_row
                and board[nr2][col] == "."
            ):
                moves.append((nr2, col))

        # Diagonal captures only.
        for dc in (-1, 1):
            nr = row + direction
            nc = col + dc

            if inside(nr, nc) and enemy(
                piece, board[nr][nc]
            ):
                moves.append((nr, nc))

        return moves

    if kind == "N":
        for dr, dc in (
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ):
            nr = row + dr
            nc = col + dc

            if not inside(nr, nc):
                continue

            if not same_side(piece, board[nr][nc]):
                moves.append((nr, nc))

        return moves

    directions = []

    if kind == "B":
        directions = [
            (-1, -1), (-1, 1),
            (1, -1), (1, 1)
        ]

    elif kind == "R":
        directions = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1)
        ]

    elif kind == "Q":
        directions = [
            (-1, -1), (-1, 1),
            (1, -1), (1, 1),
            (-1, 0), (1, 0),
            (0, -1), (0, 1)
        ]

    elif kind == "K":
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

    for dr, dc in directions:
        nr, nc = row + dr, col + dc

        while inside(nr, nc):
            target = board[nr][nc]

            # Never move onto your own piece.
            if same_side(piece, target):
                break

            moves.append((nr, nc))

            # Stop after capturing an enemy piece.
            if target != ".":
                break

            # King moves only one square.
            if kind == "K":
                break

            nr += dr
            nc += dc

    return moves


def legal_moves(board, row, col):
    """
    Filter pseudo-moves so the player's own King
    cannot remain in check.
    """
    piece = board[row][col]

    if piece == ".":
        return []

    white = piece.isupper()
    result = []

    for nr, nc in pseudo_moves(board, row, col):
        copy_board = [r[:] for r in board]

        copy_board[nr][nc] = copy_board[row][col]
        copy_board[row][col] = "."

        if not is_in_check(copy_board, white):
            result.append((nr, nc))

    return result


def mouse_to_square(pos):
    x, y = pos

    if not (
        BOARD_X <= x < BOARD_X + BOARD_SIZE
        and BOARD_Y <= y < BOARD_Y + BOARD_SIZE
    ):
        return None

    col = (x - BOARD_X) // SIZE
    row = (y - BOARD_Y) // SIZE

    return row, col


def draw_text(text, font, position, color=DEEP_BLUE, center=False):
    image = font.render(text, True, color)
    rect = image.get_rect()

    if center:
        rect.center = position
    else:
        rect.topleft = position

    screen.blit(image, rect)


def draw_board(board, selected, moves, turn, game_over=False):
    screen.fill(BACKGROUND)

    draw_text(
        "CHECKMATE",
        font_title,
        (WIDTH // 2, 45),
        DEEP_BLUE,
        center=True
    )

    draw_text(
        "BLUE & WHITE EDITION",
        font_small,
        (WIDTH // 2, 80),
        DARK_BLUE,
        center=True
    )

    # Clear side labels
    draw_text(
        "BLACK",
        font_small,
        (BOARD_X + BOARD_SIZE // 2, 105),
        BLACK_PIECE,
        center=True
    )

    draw_text(
        "WHITE",
        font_small,
        (BOARD_X + BOARD_SIZE // 2, 805),
        DEEP_BLUE,
        center=True
    )

    pygame.draw.rect(
        screen,
        SHADOW,
        (
            BOARD_X + 8,
            BOARD_Y + 8,
            BOARD_SIZE + 10,
            BOARD_SIZE + 10
        ),
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        DARK_BLUE,
        (
            BOARD_X - 5,
            BOARD_Y - 5,
            BOARD_SIZE + 10,
            BOARD_SIZE + 10
        ),
        border_radius=12
    )

    for row in range(8):
        for col in range(8):
            x = BOARD_X + col * SIZE
            y = BOARD_Y + row * SIZE

            color = (
                WHITE_SQUARE
                if (row + col) % 2 == 0
                else BLUE_SQUARE
            )

            pygame.draw.rect(
                screen,
                color,
                (x, y, SIZE, SIZE)
            )

    # Highlight legal moves.
    for row, col in moves:
        x = BOARD_X + col * SIZE
        y = BOARD_Y + row * SIZE

        pygame.draw.circle(
            screen,
            MOVE_BLUE,
            (x + SIZE // 2, y + SIZE // 2),
            12
        )

    # Highlight selected piece.
    if selected is not None:
        row, col = selected
        x = BOARD_X + col * SIZE
        y = BOARD_Y + row * SIZE

        pygame.draw.rect(
            screen,
            SELECT_BLUE,
            (x + 3, y + 3, SIZE - 6, SIZE - 6),
            5
        )

    # Draw pieces.
    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece == ".":
                continue

            x = BOARD_X + col * SIZE + SIZE // 2
            y = BOARD_Y + row * SIZE + SIZE // 2

            if piece.isupper():
                piece_bg = WHITE_PIECE
                piece_color = DEEP_BLUE
                outline = WHITE_PIECE_OUTLINE
            else:
                piece_bg = BLACK_PIECE
                piece_color = pygame.Color("white")
                outline = BLACK_PIECE_OUTLINE

            pygame.draw.circle(screen, piece_bg, (x, y), 29)
            pygame.draw.circle(screen, outline, (x, y), 29, 2)

            # Highlight King in check.
            if (
                piece == ("K" if turn else "k")
                and is_in_check(board, turn)
            ):
                pygame.draw.circle(screen, RED, (x, y), 34, 4)
                piece_color = RED if piece.isupper() else RED

            draw_text(
                piece.upper(),
                font_piece,
                (x, y),
                piece_color,
                center=True
            )

    if game_over:
        overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
        overlay.fill((20, 45, 70, 180))
        screen.blit(overlay, (BOARD_X, BOARD_Y))

        draw_text(
            "FAIL",
            font_gameover,
            (WIDTH // 2, BOARD_Y + 275),
            RED,
            center=True
        )
        draw_text(
            "GAME OVER",
            font_title,
            (WIDTH // 2, BOARD_Y + 340),
            pygame.Color("white"),
            center=True
        )
        draw_text(
            "Press R to restart",
            font_small,
            (WIDTH // 2, BOARD_Y + 395),
            pygame.Color("white"),
            center=True
        )
    else:
        turn_text = "WHITE'S TURN" if turn else "BLACK'S TURN"

        if is_in_check(board, turn):
            status = f"{turn_text} - CHECK!"
            status_color = RED
        elif selected is not None:
            status = f"{turn_text} - choose a highlighted square"
            status_color = DARK_BLUE
        else:
            status = f"{turn_text} - click a piece"
            status_color = DEEP_BLUE

        draw_text(
            status,
            font_small,
            (WIDTH // 2, 860),
            status_color,
            center=True
        )

    # Legend: which symbols belong to which side
    draw_text(
        "WHITE: K Q R B N P",
        font_small,
        (20, 35),
        DEEP_BLUE
    )

    draw_text(
        "BLACK: k q r b n p",
        font_small,
        (WIDTH - 210, 35),
        BLACK_PIECE
    )


def main():
    board = [row[:] for row in START_BOARD]

    selected = None
    moves = []
    turn = True  # White starts.
    game_over = False

    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                board = [row[:] for row in START_BOARD]
                selected = None
                moves = []
                turn = True
                game_over = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    continue

                square = mouse_to_square(event.pos)

                if square is None:
                    continue

                row, col = square
                piece = board[row][col]

                if selected is None:
                    # Can only select the side whose turn it is.
                    if (
                        piece != "."
                        and piece.isupper() == turn
                    ):
                        selected = (row, col)
                        moves = legal_moves(
                            board, row, col
                        )

                else:
                    if square in moves:
                        sr, sc = selected

                        board[row][col] = board[sr][sc]
                        board[sr][sc] = "."

                        # Promote a pawn to a Queen at the far rank.
                        if board[row][col] == "P" and row == 0:
                            board[row][col] = "Q"
                        elif board[row][col] == "p" and row == 7:
                            board[row][col] = "q"

                        selected = None
                        moves = []

                        # Switch turns after a valid move.
                        turn = not turn

                        # Requested game rule: any checked King ends the game.
                        if is_in_check(board, turn):
                            # Rush00 function: Success means the white King is in check.
                            # The GUI intentionally displays FAIL as the game-over message.
                            checkmate(board_string(board))
                            game_over = True

                    elif (
                        piece != "."
                        and piece.isupper() == turn
                    ):
                        # Select another own piece.
                        selected = (row, col)
                        moves = legal_moves(
                            board, row, col
                        )

                    else:
                        selected = None
                        moves = []

        draw_board(board, selected, moves, turn, game_over)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
