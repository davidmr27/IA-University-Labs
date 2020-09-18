import numpy as np
import random as rd
import xlrd

from pyknon.genmidi import Midi
from pyknon.music import NoteSeq, Note, Rest

LEN_OF_MUSIC = 200


class Music:
    def __init__(self, notes, beats):
        self.notes = notes
        self.beats = beats


class MarkovNotes:
    notes = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10,
             "B": 11 , "0": 101}
    beats = {"0": 0, "1": (1 / 16), "2": (1 / 8), "3": (1 / 4), "4": (1 / 16), "5": (1 / 2), "6": (1 / 32), "7": 1}

    def __init__(self):
        self.LEN_MUSIC = 200
        self.transition_notes = None
        self.keys_notes = []
        self.transition_beats = None
        self.keys_beats = []
        self.sum_tran_notes = None
        self.sum_tran_beats = None
        self.notes_number = []
        self.beats_number = []

    def generate_universe(self, music_notes, beats):
        duplicates_notes = {}
        duplicates_beats = {}
        for char in range(len(music_notes)):
            if music_notes[char] in duplicates_notes:
                duplicates_notes[music_notes[char]] += 1
            else:
                duplicates_notes[music_notes[char]] = 1

        for char in range(len(beats)):
            if beats[char] in duplicates_beats:
                duplicates_beats[beats[char]] += 1
            else:
                duplicates_beats[beats[char]] = 1

        self.keys_notes = list(duplicates_notes.keys())
        self.transition_notes = np.zeros((len(self.keys_notes), len(self.keys_notes)), dtype=float)

        self.keys_beats = list(duplicates_beats.keys())
        self.transition_beats = np.zeros((len(self.keys_beats), len(self.keys_beats)), dtype=float)

    def sum_transition(self, music_notes, beats):
        self.convert_to_number(music_notes, beats)
        values = self.notes_number
        v_beats = self.beats_number
        for (i, j) in zip(values, values[1:]):
            self.transition_notes[i][j] += 1

        for (i, j) in zip(v_beats, v_beats[1:]):
            self.transition_beats[i][j] += 1

    def convert_to_number(self, music_notes, beats):
        for i in music_notes:
            index = self.keys_notes.index(i)
            self.notes_number.append(index)

        for i in beats:
            index = self.keys_beats.index(i)
            self.beats_number.append(index)

    def convert_to_probability(self):
        self.sum_tran_notes = np.sum(self.transition_notes, axis=1)
        self.sum_tran_beats = np.sum(self.transition_beats, axis=1)

        for i in range(len(self.keys_notes)):
            for j in range(len(self.keys_notes)):
                if self.sum_tran_notes[i] == 0.:
                    break
                self.transition_notes[i][j] = self.transition_notes[i][j] / self.sum_tran_notes[i]

        for i in range(len(self.keys_beats)):
            for j in range(len(self.keys_beats)):
                if self.sum_tran_beats[i] == 0.:
                    break
                self.transition_beats[i][j] /= self.sum_tran_beats[i]

    def predict_next_note(self, note):
        index = self.keys_notes.index(note)
        single_note = np.random.choice(self.keys_notes, p=self.transition_notes[index])
        return single_note

    def predict_next_beat(self, beat):
        index = self.keys_beats.index(beat)
        single_beat = np.random.choice(self.keys_beats, p=self.transition_beats[index])
        return single_beat

    def convert_to_beat(self, beats_of_music):
        list_beat = []
        for i in range(self.LEN_MUSIC):
            list_beat.append(self.beats[str(beats_of_music[i])])
        return list_beat

    def convert_to_notes(self, notes_of_music):
        list_notes = []
        for i in range(self.LEN_MUSIC):
            list_notes.append(self.notes[str(notes_of_music[i])])
        return list_notes

    def generate_music(self):
        seq_notes = []
        value = ""
        seq_notes.append("".join(rd.sample(self.keys_notes, 1)))
        for i in range(self.LEN_MUSIC):
            if i > 0:
                value = "".join(seq_notes[i - 1])
                # print("{} {}".format(type(value), value))
                seq_notes.append(self.predict_next_note(value))
            value = ""
        return seq_notes

    def generate_music_time(self):
        seq_notes = []
        seq_beats = []
        prev_note = ""
        prev_beat = 0
        seq_notes.append("".join(rd.sample(self.keys_notes, 1)))
        seq_beats.append((rd.sample(self.keys_beats, 1).pop()))
        for i in range(self.LEN_MUSIC):
            if i > 0:
                prev_note = "".join(seq_notes[i - 1])
                prev_beat = seq_beats[i - 1]
                # print(type(prev_beat.pop()))
                seq_notes.append(self.predict_next_note(prev_note))
                seq_beats.append(self.predict_next_beat(prev_beat))
            prev_note = ""
            prev_beat = 0

        seq_beats = self.convert_to_beat(seq_beats)
        seq_notes = self.convert_to_notes(seq_notes)
        return seq_notes, seq_beats


def create_midi_without_time(music):
    seq_notes = " ".join(music)
    seq = NoteSeq(seq_notes)
    midi = Midi(number_tracks=1, tempo=90)
    midi.seq_notes(seq, track=0)
    midi.write("midi/markov_test.mid")


def create_midi_with_time(music, beat_of_music):
    global LEN_OF_MUSIC
    noteSeq = []
    for i in range(LEN_OF_MUSIC):
        if music[i] == 101:
            noteSeq.append(Rest(dur=beat_of_music[i]))
        else:
            noteSeq.append(Note(music[i], dur=beat_of_music[i]))

    seq = NoteSeq(noteSeq)
    midi = Midi(number_tracks=1, tempo=90)
    midi.seq_notes(seq, track=0)
    midi.write("midi/markov_Gavotte_test1.mid")


def upload_data_excel():
    music = []
    notes = []
    beats = []

    loc = "beats.xlsx"
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    for i in range(sheet.ncols):
        if (i % 2) == 1:
            continue
        for j in range(sheet.nrows):
            if sheet.cell_value(j, i) != '':
                if sheet.cell_value(j, i) == 0.0:
                    notes.append('0')
                else:
                    notes.append(sheet.cell_value(j, i))
                beats.append(int(sheet.cell_value(j, i + 1)))

        music.append(Music(notes, beats))
        notes = []
        beats = []

    return music


markov = MarkovNotes()

notes = upload_data_excel()
notes_file = notes[7].notes
beats = notes[7].beats

markov.generate_universe(notes_file, beats)
markov.sum_transition(notes_file, beats)
markov.convert_to_probability()

print(markov.keys_beats)
print(markov.transition_beats)

music, beat = markov.generate_music_time()
create_midi_with_time(music, beat)
# print("{}".format(music))
# create_midi(music)
