"""This module is responsible for playing audio."""


AUDIO_DIR = "Audio"


import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from scipy.io import wavfile
import pygame
import chess


def play_audio(audio_file: str):
    """Play an arbitrary wav-audio in the "Audio" directory.

    :param audio_file: Filename of the audio file (including the '.wav' extension).
    """
    try:
        fs, _ = wavfile.read(AUDIO_DIR + "/" + audio_file)
        pygame.mixer.init(frequency=fs)
        pygame.mixer.music.load(AUDIO_DIR + "/" + audio_file)
    except FileNotFoundError:
        try:  # This happens when we run this file from the "lpspectator" directory in the terminal
            fs, _ = wavfile.read("../" + AUDIO_DIR + "/" + audio_file)
            pygame.mixer.init(frequency=fs)
            pygame.mixer.music.load("../" + AUDIO_DIR + "/" + audio_file)
        except FileNotFoundError:
            import sys

            print(
                f'Please make sure "{audio_file}" exists in the "{AUDIO_DIR}" directory!'
            )
            sys.exit()
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    pygame.mixer.quit()


def play_checkmate_audio():
    """Play the audio associated with checkmate."""
    play_audio("Boom!.wav")
    play_audio("That_s_not_just_a_check__that_is_a_big_checkmate!.wav")


def play_critical_moment_audio():
    """Play the audio associated with critical moments."""
    play_audio("This_is_a_critical_moment.wav")


def play_stalemate_audio():
    """Play the audio associated with stalemate."""
    play_audio("God_stalemate!.wav")


def play_harry_audio():
    """Play the audio associated with pushing Harry the h-pawn."""
    play_audio("Look_at_Harry_Come_on_Harry!.wav")


def play_lobsterpincer_audio():
    """Play the audio associated with the Lobster Pincer mate."""
    play_audio("Boom!.wav")
    play_audio("Oh!.wav")
    play_audio("Oh_yes!.wav")
    play_audio("This_is_how_you_win_a_game.wav")
    play_audio("Lobsterpincer_mate.wav")
    play_audio("Let_s_go!.wav")


def play_move_sound_effect():
    """Play the sound effect associated with making a move."""
    play_audio("Move_sound_effect.wav")


def play_capture_sound_effect():
    """Play the sound effect associated with making a capture."""
    play_audio("Capture_sound_effect.wav")


def play_castling_sound_effect():
    """Play the sound effect associated with castling."""
    play_audio("Castling_sound_effect.wav")


def play_check_sound_effect():
    """Play the sound effect associated with check."""
    play_audio("Check_sound_effect.wav")


def play_promotion_sound_effect():
    """Play the sound effect associated with promotion."""
    play_audio("Promotion_sound_effect.wav")


def play_checkmate_sound_effect():
    """Play the sound effect associated with checkmate."""
    play_audio("Checkmate_sound_effect.wav")


def play_promotion_with_checkmate_sound_effect():
    """Play the sound effect associated with promotion with checkmate."""
    play_audio("Promotion_with_checkmate_sound_effect.wav")


def play_sound_effect_for_detected_move(board: chess.Board, detected_move: chess.Move):
    """Play the sound effect for the detected move."""
    if board.is_checkmate():
        if detected_move.promotion is not None:
            play_promotion_with_checkmate_sound_effect()
        else:
            play_checkmate_sound_effect()
    elif board.is_check():
        play_check_sound_effect()
    else:
        board.pop()
        if board.is_castling(detected_move):
            play_castling_sound_effect()
        elif detected_move.promotion is not None:
            play_promotion_sound_effect()
        elif board.is_capture(detected_move):
            play_capture_sound_effect()
        else:
            play_move_sound_effect()
        board.push(detected_move)


if __name__ == "__main__":
    play_critical_moment_audio()

    play_stalemate_audio()

    play_harry_audio()

    play_move_sound_effect()

    play_capture_sound_effect()

    play_castling_sound_effect()

    play_check_sound_effect()

    play_promotion_sound_effect()

    play_promotion_with_checkmate_sound_effect()

    play_checkmate_audio()

    play_checkmate_sound_effect()

    play_lobsterpincer_audio()

    board = chess.Board()
    detected_move = chess.Move.from_uci("d2d4")
    board.push(detected_move)
    play_sound_effect_for_detected_move(board, detected_move)
