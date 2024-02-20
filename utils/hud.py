from utils.colors import BLACK
from fonts import screen_font


def draw_hud(screen_w, screen, scr1, scr2, time_elapsed, max_time):
    # player 1 score
    score_1_txt = f"Score: {scr1}"
    score_1 = screen_font.render(score_1_txt, True, BLACK)
    screen.blit(score_1, (10, 10))
    # player 2 score
    score_2_txt = f"Score: {scr2}"
    score_2 = screen_font.render(score_2_txt, True, BLACK)
    score_2_rect = score_2.get_rect()
    score_2_rect.right = screen_w - 10
    score_2_rect.top = 10
    # draw scores
    screen.blit(score_2, score_2_rect)
    # Calculate the remaining time and draw in the top center corner
    time_remaining = max_time - time_elapsed
    minutes = time_remaining // 60
    seconds = time_remaining % 60
    time_txt = f"Time: {minutes:02}:{seconds:02}"
    time = screen_font.render(time_txt, True, BLACK)
    time_rect = time.get_rect()
    time_rect.centerx = screen_w // 2
    time_rect.top = 10
    screen.blit(time, time_rect)
