import random
import string
class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn

        # You should keep updating following variable with best string so far .
        self.best_state = None
        self.InverseMatrix = []
    def assignSubstring(self,s,i,j,v):
        return s[0:i]+v+s[j+1:]
    def giveChar(self,i,start_state):
        c = start_state[i]
        chars = self.conf_matrix[start_state[i]]
        cost = (len(chars)+1)*[0]
        cost[0] = self.cost_fn(start_state)
        for k in range(len(chars)):
            start_state = start_state [:i]+chars[k]+start_state[i+1:]
            cost[k+1] = self.cost_fn(start_state)
        m = cost[0]
        j = 0
        for k in range(1,len(chars)+1):
            if(cost[k] < m):
                m = cost[k]
                j = k
        if(j==0):
            return c
        else:
            return chars[j-1]
    def sortfun(self,e):
        return e[1]
    def beamSearch(self,states,i,n,start_state):
        self.best_state = states[0]
        if(i==n):
            return states[0]
        if(start_state[i] == ' '):
            return self.beamSearch(states,i+1,n,start_state)
        char = []
        if self.InverseMatrix.get(start_state[i]) == None:
            char = self.conf_matrix[start_state[i]]
        else:
            char = self.InverseMatrix[start_state[i]]
        chars = [start_state[i]] + char
        newstates = []
        for state in states:
            for c in chars:
                state = state[:i]+c+state[i+1:]
                newstates.append([state,self.cost_fn(state)])
        newstates.sort(key=self.sortfun)
        nextstates =[]
        k = 35
        if(k>len(newstates)):
            k = len(newstates)
        for j in range(k):
            nextstates.append(newstates[j][0])
        return self.beamSearch(nextstates,i+1,n,start_state)

    # Matrix Inverstion
    def Inverse(self):
        self.InverseMatrix = {}
        for key, value in  self.conf_matrix.items():
            for string in value:
                self.InverseMatrix.setdefault(string, []).append(key)

    def search(self, start_state):
        """
        :param start_state: str Input string with spelling errors
        """
        # You should keep updating self.best_state with best string so far.
        # self.best_state = start_state
        self.Inverse()

        # Beam Search Implemention
        states = []
        states.append(start_state)
        char = []
        if self.InverseMatrix.get(start_state[0]) != None:
            char = self.InverseMatrix[start_state[0]]
        chars = self.conf_matrix[start_state[0]] + char
        for c in chars:
            start_state = c + start_state[1:]
            states.append(start_state)
        final_state = self.beamSearch(states,1,len(start_state),start_state)
        start_state = final_state

        # Hill Climbing Implementation
        for i in range(len(start_state)-1,-1,-1):
            if(start_state[i]==' '):
                continue
            start_state = start_state[:i]+self.giveChar(i,start_state)+start_state[i+1:]
            self.best_state = start_state

        # Random Search Implementation
        n = len(start_state) - 1
        alphabet_string = string.ascii_lowercase
        chars = list(alphabet_string)
        while(True):
            r = random.randint(0,n)
            if(start_state[r]==' '):
                continue
            r2 = random.randint(0,25)
            new_state = start_state[:r]+chars[r2]+start_state[r+1:]
            if(self.cost_fn(new_state)<self.cost_fn(start_state)):
                start_state =  new_state
                self.best_state = new_state
        return start_state
        raise Exception("Not Implemented.")
