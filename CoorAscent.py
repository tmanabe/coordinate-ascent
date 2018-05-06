from random import shuffle


class Params(dict):
    pass


class CoorAscent(object):
    def __init__(self,
                 evaluate,
                 validate = None,
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
        regParams = params.copy()
        globalBestParams, globalBestScore = regParams, self.evaluate(regParams)
        assert globalBestScore is not None
        signs = [1, -1, 0]

        for r in range(self.nRestart):
            consecutive_fails = 0
            params, startScore = regParams.copy(), self.evaluate(params)
            current_feature = -1
            bestParams, bestScore = params.copy(), startScore
            while(1 < len(params) and consecutive_fails < len(params) - 1 or
                  1 == len(params) and 0 == consecutive_fails):
                fids = list(params.keys())
                shuffle(fids)
                for current_feature in fids:
                    origParam = params[current_feature]
                    totalStep, bestTotalStep = 0.0, 0.0
                    succeeds = False
                    for dir in signs:
                        step = 0.001 * dir
                        if 0.0 != origParam and 0.5 * abs(origParam) < abs(step):
                            step = self.stepBase * abs(origWeight)
                        totalStep = step
                        self.numIter = self.nMaxIteration
                        if 0 == dir:
                            numIter = 1
                            totalStep = -origParam
                        for j in range(self.numIter):
                            w = origParam + totalStep
                            param_change = step
                            params[current_feature] = w
                            score = self.evaluate(params)
                            if score is not None and bestScore < score:
                                bestScore = score
                                bestTotalStep = totalStep
                                succeeds = True
                            if j < self.nMaxIteration - 1:
                                step *= self.stepScale
                                totalStep += step
                        if(succeeds):
                            break
                        elif(signs[-1] == dir):
                            weight_change = -totalStep
                            params[current_feature] = origParam
                    if succeeds:
                        consecutive_fails = 0
                        param_change = bestTotalStep - totalStep
                        params[current_feature] = origParam + bestTotalStep
                        bestParams = params.copy()
                    else:
                        consecutive_fails += 1
                        param_change = -totalStep
                        params[current_feature] = origParam
                if (bestScore - startScore < self.tolerance):
                    break
            if self.validate is not None:
                current_feature = -1
                bestScore = self.validate(bestParams)
            if globalBestScore < bestScore:
                globalBestScore, globalBestParams = bestScore, bestParams.copy()
        return globalBestParams


if __name__ == '__main__':
    params = Params()
    params['x'] = 1.0
    params['y'] = 10.0
    params['z'] = 100.0

    e = lambda params: -((params['x'] + 1) ** 2 + (params['y'] + 10) ** 2 + (params['z'] + 100) ** 2)

    ca = CoorAscent(e)
    print(ca.learn(params))