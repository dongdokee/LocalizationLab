from typing import Dict, Tuple, Union

# dictionary key로는 y가 특정 점이면 중복되지 않는 아무 str, 영역이면 중복되지 않는 영역 이름 str
# dictionary value로는 y가 특정 점이면 float 2개 (x, y), 영역이면 float 4개 (x1, y1, x2, y2)
y_def: Dict[str, Tuple[float, float] | Tuple[float, float, float, float]] = {
    "1": (0.33, 0.33),
    "2": (0.33, 0.66),
    "3": (0.66, 0.33),
    "4": (0.66, 0.66),
}
