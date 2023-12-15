class Game:
    def __init__(self) -> None:
        self.countForest = 5
        self.standard_prob = 5
        self.chance_find_battle = 5
        self.final_boss = 1
    
    def lowerCountForest(self) -> None:
        self.countForest = self.countForest - 1 
    
    def checkForestSafe(self) -> bool:
        return (self.countForest == 0)
    
    def checkIfFinalBossDefeated(self) -> bool:
        return (self.final_boss == 0)
    
    def enterBattleFinalBoss(self) -> None:
        self.final_boss = 0