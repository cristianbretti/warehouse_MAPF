## TEMP:
from create_graphs import *

from AStar import *
from functions import *

class State(object):
    def __init__(self, agent1, agent2, agents):
        self.agent1 = agent1
        self.agent2 = agent2
        self.agents = agents

class Simulation(object):
    def __init__(self, graph, agents, workers):
        self.graph = graph
        self.agents = agents
        self.workers = workers
        self.cost = 0
        for agent in self.agents:
            if agent.pickup:
                agent.path = AStar(self.graph, agent)

    def run(self):
        done = False
        print("here")
        while(not done):
            self.cost += 1
            for agent in self.agents:
                if not agent.pickup:
                    continue
                agent.one_step_in_path()

                if agent.done_with_target():
                    if not agent.pickup.advance_pickup_state(workers, agent.is_copy):
                        #Delivered back shelf
                        if not assign_item_to_agent(agent, workers):
                            agent.pickup = None
                            agent.is_carrying_shelf = False
                    if agent.pickup:
                        agent.is_carrying_shelf = agent.pickup.is_carrying_shelf()

                    agent.path = AStar(self.graph, agent)

            agent1, agent2 = self.agents_will_collide_next_step()
            if agent1:
                return State(agent1, agent2, self.agents), self.cost, done

            done = not one_agent_has_pickup()

        return None, self.cost, done

    def agents_will_collide_next_step(self):
        for i in range(0, len(self.agents)):
            for j in range(i, len(self.agents)):
                agent1 = self.agents[i]
                agent2 = self.agents[j]

                if agent1.path[1] == agent2.path[1]:
                    return agent1, agent2
        return None, None
