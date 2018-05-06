# coordinate-ascent
Yet another implementation of Coordinate Ascent in Python.

## Quick Example

```python
# Minimize (x + 1)^2 + (y + 10)^2 + (z + 100)^2 where -50 <= z

from CoorAscent import Params, CoorAscent

params = Params()
params['x'] = 1.0
params['y'] = 23.0
params['z'] = 456.0  # Arbitrary initial values

def e(ps):
    if ps['z'] < -50.0:
        return None  # For invalid parameter values
    return -((ps['x'] + 1) ** 2 + (ps['y'] + 10) ** 2 + (ps['z'] + 100) ** 2)

print(CoorAscent(e).learn(params))
# => {'x': -1.0, 'y': -10.0, 'z': -50.0}
```

## References
- RankLib https://sourceforge.net/p/lemur/wiki/RankLib/
- D\. Metzler and W.B. Croft. Linear feature-based models for information retrieval. _Information Retrieval_, 10(3): 257-274, 2007.
