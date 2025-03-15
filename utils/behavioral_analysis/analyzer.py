class BehaviorAnalyzer:
    def analyze(self, user_actions):
        return {"most_frequent_action": max(set(user_actions), key=user_actions.count)}
