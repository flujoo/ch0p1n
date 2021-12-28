"""
Elaborate and repeat (vary) motifs.
"""

from typing import Union, List, Optional
from copy import deepcopy

Pitch = int
PitchClass = int
PitchLine = List[Union[Pitch, None, List[Pitch]]]

# the term "pitch line" denotes the pitch content of musical line
# the same goes for "duration line"

Duration = Union[int, float]
DurationLine = List[Duration]



# move single pitches ------------------------------------------

def _reify(scale: List[PitchClass]) -> List[Pitch]:

    """
    Turn a scale into its whole range of pitches.
    """

    scale.sort()

    pitches = [
        pitch_class + octave*12
        for octave in range(11)
        for pitch_class in scale
    ]

    return pitches


def _move(
        pitch: Optional[Pitch],
        scale: List[Pitch], # reified
        step: int
    ) -> Optional[Pitch]:

    """
    Move a pitch along a scale by certain number of steps.
    """

    if pitch is None:
        return None

    if pitch not in scale:
        if step == 0:
            # rather than trigger an error
            return None
        else:
            # insert `pitch` into `scale`
            scale.append(pitch)
            scale.sort()

    i = scale.index(pitch)

    # move `pitch`
    pitch = scale[i + step]

    return pitch


def _move2(
        pitch: Optional[Pitch],
        scale: List[Pitch],
        steps: List[int]
    ) -> List[Optional[Pitch]]:

    """
    Move a pitch along a scale by different numbers of steps.
    """

    if pitch is None:
        return [None]

    if not steps:
        return []

    if (pitch not in scale) and (0 in steps):
        steps = [step for step in steps if step != 0]

    pitches = [_move(pitch, scale, step) for step in steps]
    return pitches



# extract and replace pitches ----------------------------------

def _extract(pitch_motif: PitchLine) -> List[Optional[Pitch]]:

    """
    Extract pitches from a pitch motif.
    """

    pitches = []

    for item in pitch_motif:
        if isinstance(item, list):
            pitches.extend(item)
        else:
            pitches.append(item)

    return pitches


def _replace(
        pitch_motif: PitchLine,
        pitches: List[Optional[Pitch]],
        in_place: bool = False
    ) -> Optional[PitchLine]:

    """
    Replace the pitches of a motif.
    """

    if not in_place:
        pitch_motif = deepcopy(pitch_motif)

    k = 0

    for i, item in enumerate(pitch_motif):
        if isinstance(item, list):
            l = len(item)
            pitch_motif[i] = pitches[k:k+l]
            k = k + l
        else:
            pitch_motif[i] = pitches[k]
            k = k + 1

    if not in_place:
        return pitch_motif



# repeat pitch motifs ------------------------------------------

def transpose(
        pitch_motif: PitchLine,
        scale: List[PitchClass],
        step: int
    ) -> PitchLine:

    """
    Transpose a pitch motif along a given scale
    by a certain number of steps.
    """
    
    scale = _reify(scale)
    pitches = _extract(pitch_motif)

    pitches = [
        _move(pitch, scale, step)
        for pitch in pitches
    ]

    motif = _replace(pitch_motif, pitches)
    return motif
