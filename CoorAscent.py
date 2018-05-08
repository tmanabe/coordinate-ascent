from random import shuffle


class CoorAscent(object):
    def __init__(self,
                 evaluate,
                 validate=None,
                 nRestart=5,
                 nMaxIteration=25,
                 stepBase=0.05,
                 stepScale=2.0,
                 tolerance=0.001):
        assert 'function' == evaluate.__class__.__name__
        self.evaluate = evaluate
        if validate is not None:
            assert 'function' == validate.__class__.__name__
        self.validate = validate

        self.nRestart = nRestart
        self.nMaxIteration = nMaxIteration
        self.stepBase = stepBase
        self.stepScale = stepScale
        self.tolerance = tolerance

    def learn(self, params):
        keys = list(params.keys())
        regularParams, globalStartScore = params.copy(), self.evaluate(params)
        assert globalStartScore is not None
        globalBestParams, globalBestScore = regularParams.copy(), globalStartScore

        for _ in range(self.nRestart):
            consecutiveFails = 0
            params = regularParams.copy()
            bestParams, bestScore = regularParams.copy(), globalStartScore

            while consecutiveFails < len(keys):
                startScore = bestScore
                shuffle(keys)

                for currentKey in keys:
                    originalValue, bestTotalStep, succeeds = params[currentKey], 0.0, False

                    for direction in [1, -1, 0]:
                        step = 0.001 * direction
                        if 0.0 != originalValue and abs(originalValue) < 2 * abs(step):
                            step = self.stepBase * abs(originalValue)
                        totalStep, nIteration = step, self.nMaxIteration
                        if 0 == direction:
                            totalStep, nIteration = -originalValue, 1

                        for _ in range(nIteration):
                            params[currentKey] = originalValue + totalStep
                            score = self.evaluate(params)
                            if score is not None and bestScore < score:
                                bestScore, bestTotalStep, succeeds = score, totalStep, True
                            step *= self.stepScale
                            totalStep += step

                        if succeeds:
                            break

                    if succeeds:
                        consecutiveFails = 0
                        params[currentKey] = originalValue + bestTotalStep
                        bestParams = params.copy()
                    else:
                        consecutiveFails += 1
                        params[currentKey] = originalValue

                if (bestScore - startScore < self.tolerance):
                    break

            if self.validate is not None:
                bestScore = self.validate(bestParams)
            if globalBestScore < bestScore:
                globalBestScore, globalBestParams = bestScore, bestParams.copy()

        return globalBestParams


if __name__ == '__main__':
    from CoorAscent import CoorAscent

    def e(params):  # Objective function
        # Minimize (x+1)^2 + (y+10)^2 + (z+100)^2 where -50 <= z
        if not -50 <= params['z']:
            return None  # For invalid parameter values
        return -((params['x'] + 1) ** 2 + (params['y'] + 10) ** 2 + (params['z'] + 100) ** 2)

    params = {'x': 1.0, 'y': 23.0, 'z': 456.0}  # Arbitrary initial values

    print(CoorAscent(e).learn(params))  # => {'x': -1.0, 'y': -10.0, 'z': -50.0}
