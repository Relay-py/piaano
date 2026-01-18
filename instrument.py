import fluidsynth
from SoundButton2 import SoundButton


class Instrument:

    def __init__(self, soundfont_path: str, initial_bank=0, initial_preset=0, volume=50):
        self.current_notes = set()

        # create synthesizer object
        self.fs = fluidsynth.Synth()

        # load soundfont and all sounds
        self.soundfont_path = soundfont_path
        self.sfid = self.fs.sfload(self.soundfont_path)

        # set initial bank and preset
        self.preset = initial_preset
        self.bank = initial_bank
        self.volume = volume

    # def generate_soundbuttons(self, group_top_left, size, padding):
    #     """
    #     return list of buttons from the sounds in the soundfont
    #     """
    #     buttons = []
    #     for b in range(2):
    #         for p in range(5):
    #             buttons.append(
    #                 SoundButton(top_left=(group_top_left[0] + (size[0] + padding[0]) * b,
    #                                       group_top_left[1] + (size[1] + padding[1]) * p),
    #                             size=size,
    #                             sound=(b, p),
    #                             text=self.fs.sfpreset_name(self.sfid, b, p),
    #                             colour="steelblue1"))
    #     return buttons
    def generate_soundbuttons(self, group_top_left, size, padding):
        """
        Creates a list of neon-styled buttons.
        Assigns different colors based on the instrument bank.
        """
        buttons = []
        
        # Color palette matching your Spark and RisingNote colors
        # Bank 0: Pianos (Cyan)
        # Bank 1: Synths/Others (Magenta)
        bank_colors = {
            0: (0, 220, 255),   # Cyan
            1: (255, 100, 255), # Magenta
            2: (0, 255, 150),   # Mint Green
            3: (255, 255, 100)  # Yellow
        }

        for b in range(2):  # Loop through banks
            # Pick the color for this specific bank
            current_color = bank_colors.get(b, (200, 200, 200))
            
            for p in range(5):  # Loop through presets
                # Calculate position
                pos_x = group_top_left[0] + (size[0] + padding[0]) * b
                pos_y = group_top_left[1] + (size[1] + padding[1]) * p
                
                # Fetch preset name from FluidSynth
                preset_name = self.fs.sfpreset_name(self.sfid, b, p)
                if not preset_name:
                    preset_name = f"Bank {b} P {p}"

                buttons.append(
                    SoundButton(
                        top_left=(pos_x, pos_y),
                        size=size,
                        sound=(b, p),
                        text=preset_name,
                        colour=current_color  # Pass the bank-specific color
                    )
                )
        return buttons

    def start(self) -> None:
        """
        start synthesizer with current bank and preset
        """
        self.fs.setting("synth.gain", 2.0)
        self.fs.start()

        self.fs.program_select(0, self.sfid, self.bank, self.preset)

    def change_sound(self, new_sound):
        self.bank = new_sound[0]
        self.preset = new_sound[1]
        self.fs.program_select(0, self.sfid, self.bank, self.preset)

    def stop(self) -> None:
        self.fs.delete()

    def add_note(self, midi_note: int) -> None:
        self.current_notes.add(midi_note)

        self.fs.noteon(0, midi_note, self.volume)

    def remove_note(self, midi_note) -> None:
        if midi_note not in self.current_notes:
            return

        self.current_notes.remove(midi_note)
        self.fs.noteoff(0, midi_note)

    def remove_all_notes(self):
        for i in range(30, 150):
            self.remove_note(i)

    def is_playing(self, midi_note) -> bool:
        return midi_note in self.current_notes
