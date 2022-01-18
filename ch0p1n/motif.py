"""
Elaborate and repeat (vary) motifs.
"""

from typing import Union, List, Optional, Dict, Tuple, Any
from copy import deepcopy
from itertools import product

Pitch = int
PitchClass = int
# pitches and pitch classes are represented by MIDI note numbers

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
        step: Optional[int] # for `elaborate`
    ) -> Optional[Pitch]:

    """
    Move a pitch along a scale by certain number of steps.
    """

    # note that `not step` is `true` when `step` is `0`
    if (pitch is None) or (step is None):
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
        scale: List[Pitch], # reified
        steps: List[Optional[int]]
    ) -> List[Optional[Pitch]]:

    """
    Move a pitch along a scale by different numbers of steps.
    """

    if pitch is None:
        return [None]

    if (pitch not in scale) and (0 in steps):
        steps = [step for step in steps if step != 0]
        # `steps` may be empty now,
        # so the next clause must be after this one

    if not steps:
        return []

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

def rescale(
        pitch_motif: PitchLine,
        mapping: Dict[PitchClass, PitchClass]
    ) -> PitchLine:
    
    """
    Map the pitches of a pitch motif onto a new scale.
    """

    pitches = _extract(pitch_motif)

    # map `pitches`
    for i, pitch in enumerate(pitches):
        if pitch is None:
            continue

        octave = pitch // 12
        pitch_class = pitch % 12

        if pitch_class not in mapping:
            continue

        to = mapping[pitch_class]

        # get the nearest pitch
        # for example, for mapping `{11: 0}` and pitch 59,
        # the resulted pitch should be 60 rather than 48
        d = to - pitch_class

        if d >= 6:
            to = to - 12
        elif d <= -6:
            to = to + 12

        pitches[i] = to + octave*12

    motif = _replace(pitch_motif, pitches)
    return motif


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


def lead(
        pitch_motif: PitchLine,
        harmony: List[PitchClass],
        steps: List[int] = [-1, 0, 1],
        complete: bool = True
    ) -> List[PitchLine]:
    
    """
    Repeat a pitch motif in a given harmony,
    according to the common tone rule and nearest chordal tone rule.
    """
    
    pitches = _extract(pitch_motif)
    scale = _reify(harmony)

    # get each pitch's nearest pitches
    nearest_pitches = [
        _move2(pitch, scale, steps)
        for pitch in pitches
    ]

    # combine pitches
    pitch_groups = product(*nearest_pitches)

    if complete:
        pitch_groups = [
            pitch_group for pitch_group in pitch_groups
            if _is_complete(pitch_group, harmony)
        ]

    # generate motifs
    motifs = [
        # note that `pitch_group` is tuple
        _replace(pitch_motif, list(pitch_group))
        for pitch_group in pitch_groups
    ]

    return motifs



# modify and access pitches ------------------------------------

def _modify(
        pitch_motif: PitchLine,
        position: Union[int, Tuple[int, int]],
        item: Any,
        in_place: bool = False
    ) -> Optional[PitchLine]:

    """
    Change the item of a pitch motif at the given position.
    """

    if not in_place:
        pitch_motif = deepcopy(pitch_motif)

    if isinstance(position, int):
        pitch_motif[position] = item
    else:
        i, j = position
        pitch_motif[i][j] = item

    if not in_place:
        return pitch_motif


def _access(
        line: Union[PitchLine, DurationLine],
        position: Union[int, Tuple[int, int]]
    ) -> Union[Pitch, None, List[Pitch], Duration]:
    
    """
    Get the item at the given position from a pitch or duration line.
    """

    if isinstance(position, int):
        item = line[position]
    else:
        i, j = position

        # the idea behind the following code is that
        # the position used to get item from a pitch line
        # may be re-used to get item from a duration line
        item = line[i]
        if isinstance(item, list):
            item = item[j]
    
    return item



# check harmonic completeness of pitch motifs ------------------

def _is_complete(
        pitches: Union[list, tuple],
        harmony: List[PitchClass]
    ) -> bool:
    
    """
    Check if the given pitches fully reifies the given harmony.
    """

    # get pitch classes
    pitch_classes = [pitch % 12 for pitch in pitches if pitch]

    # check completeness
    completeness = set(pitch_classes) >= set(harmony)

    return completeness


def is_complete(
        pitch_motif: PitchLine,
        harmony: List[PitchClass],
        exclude: List[Union[int, Tuple[int, int]]] = []
    ) -> bool:
    
    """
    Check if a pitch motif fully reifies the given harmony.
    """
    
    # not include the pitches at positions `exclude`
    if exclude:
        pitch_motif = deepcopy(pitch_motif)

        for position in exclude:
            _modify(pitch_motif, position, None, True)

    pitches = _extract(pitch_motif)
    completeness = _is_complete(pitches, harmony)
    return completeness



# check morphological similarity of pitch motifs ---------------

def _get_directions(pitches: List[Pitch]) -> List[int]:

    """
    Get the direction from each pitch to its next.
    """

    directions = []

    for i, pitch in enumerate(pitches[:-1]):
        d = pitches[i+1] - pitch

        if d > 0:
            directions.append(1)
        elif d < 0:
            directions.append(-1)
        else:
            directions.append(0)

    return directions


def _get_ordinals(pitches: List[Pitch]) -> List[int]:

    """
    Get the ordinals of the given pitches.
    """

    _ = sorted(set(pitches))
    ordinals = [_.index(pitch) for pitch in pitches]
    return ordinals


def _measure(
        start: Pitch,
        end: Pitch,
        scale: List[Pitch] # reified
    ) -> int:

    """
    Measure the displacement between two pitches on the given scale.
    """

    for pitch in start, end:
        if pitch not in scale:
            scale.append(pitch)

    scale.sort()

    step = scale.index(end) - scale.index(start)
    return step


def _get_steps(
        pitches: List[Pitch],
        scale: List[Pitch] # reified
    ) -> List[int]:
    
    """
    Get the displacement between each two adjacent pitches.
    """

    steps = [
        _measure(pitch, pitches[i+1], scale)
        for i, pitch in enumerate(pitches[:-1])
    ]

    return steps


def is_similar(
        pitch_motif: PitchLine,
        proto: PitchLine,
        method: str = 'direction', # 'ordinal', 'step'
        scale: List[PitchClass] = []
    ) -> bool:

    """
    Check if a pitch motif has a similar contour to the prototype.
    """

    # get the contour of a pitch motif
    def _get_contour(pitch_motif):
        
        # extract pitches
        pitches = [
            # keep only the highest pitch in a chord
            max(item) if isinstance(item, list) else item
            # remove `None`
            for item in pitch_motif if item
        ]

        # get contour
        if method == 'direction':
            contour = _get_directions(pitches)
        elif method == 'ordinal':
            contour = _get_ordinals(pitches)
        elif method == 'step':
            contour = _get_steps(pitches, scale)

        return contour

    if scale:
        scale = _reify(scale)

    similarity = _get_contour(pitch_motif) == _get_contour(proto)
    return similarity



# elaborate motifs ---------------------------------------------

def _get_i(position: Union[int, Tuple[int, int]]) -> int:

    """
    Get the first element from the given position.
    """

    if isinstance(position, tuple):
        position = position[0]

    return position


def elaborate(
        pitch_motif: PitchLine,
        duration_motif: DurationLine,
        reference: Union[int, Tuple[int, int]],
        steps: List[Optional[int]],
        scale: Optional[List[PitchClass]] = None,
        position: str = 'right', # 'left', 'previous', 'next'
        ratio: Optional[float] = None,
        relative: bool = True,
        duration: Optional[Duration] = None
    ) -> Tuple[PitchLine, DurationLine]:

    """
    Add notes or chords to the given motif.
    """

    i = _get_i(reference)
    n = len(steps)
    l = len(duration_motif)

    if duration and duration > 0:
        duration = -duration

    # add pitches ----------------------------------------------

    # get the reference pitch
    pitch = _access(pitch_motif, reference)

    # generate pitches
    pitches = []
    current = pitch
    reified = False

    for step in steps:
        if step is None:
            pitches.append(None)
        elif step == 0:
            pitches.append(current)
        else:
            if not reified:
                scale = _reify(scale)
                reified = True

            if not isinstance(current, list):
                new = _move(current, scale, step)
            else:
                new = [_move(p, scale, step) for p in current]

            pitches.append(new)

            if relative:
                current = new

    # insert `pitches`
    if position in ['left', 'previous']:
        pitches.reverse()
        pitch_motif = pitch_motif[:i] + pitches + pitch_motif[i:]
    elif position in ['right', 'next']:
        pitch_motif = pitch_motif[:i+1] + pitches + pitch_motif[i+1:]

    # add durations --------------------------------------------

    # get the reference duration
    if position in ['left', 'right']:
        duration = duration_motif[i]
    elif (position == 'previous') and (i > 0):
        duration = duration_motif[i-1]
    elif (position == 'next') and (i < l-1):
        duration = duration_motif[i+1]
    # or `duration` must be provided

    # generate durations
    if not ratio:
        durations = [duration/(n+1)] * (n+1)
    elif position in ['left', 'next']:
        durations = [duration*ratio/n]*n + [duration*(1-ratio)]
    elif position in ['right', 'previous']:
        durations = [duration*(1-ratio)] + [duration*ratio/n]*n

    # insert `durations`
    if (position == 'previous') and (i == 0):
        duration_motif = durations[1:] + duration_motif
    elif (position == 'next') and (i == l-1):
        duration_motif = duration_motif + durations[:-1]
    else:
        if position == 'previous':
            i = i - 1
        elif position == 'next':
            i = i + 1

        duration_motif = duration_motif[:i] + durations + \
            duration_motif[i+1:]

    return pitch_motif, duration_motif



# fragment motifs ----------------------------------------------

def divide(
        pitch_motif: PitchLine,
        duration_motif: DurationLine,
        n: int
    ) -> List[Tuple[PitchLine, DurationLine]]:
    
    """
    Divide a motif into parts of equal durations.
    """

    # the length of each part
    l = sum(duration_motif) / n

    motifs = []
    # current motif
    pm = []
    dm = []

    for i, duration in enumerate(duration_motif):
        # check if to start new motif
        l_dm = sum(dm)
        l_d = l_dm + duration

        if l_d <= l:
            pm.append(pitch_motif[i])
            dm.append(duration)
            if l_d == l:
                motif = pm, dm
                motifs.append(motif)
                pm = []
                dm = []
        else:
            d1 = l - l_dm
            d2 = duration - d1
            pitch = pitch_motif[i]
            pm.append(pitch)
            dm.append(d1)
            motif = pm, dm
            motifs.append(motif)
            pm = [pitch]
            dm = [d2]

    return motifs


def fragment(
        pitch_motif: PitchLine,
        duration_motif: DurationLine,
        start: int,
        end: int,
        ratio: Union[float, int, None] = None,
        fit: str = 'right' # 'left'
    ) -> Tuple[PitchLine, DurationLine]:

    """
    Take a slice of a motif. 
    """

    pm = pitch_motif[start:end+1]
    dm = duration_motif[start:end+1]

    if ratio:
        # length constraint on the motif
        l = sum(duration_motif) * ratio
        l_dm = sum(dm)
        d = l - l_dm

        if fit == 'right':
            dm[-1] = dm[-1] + d
        elif fit == 'left':
            dm[0] = dm[0] + d

    return pm, dm
