from AStar import *
from functions import *

class State(object):
    def __init__(self, agent1, agent2, agents):
        self.agent1 = agent1
        self.agent2 = agent2
        self.agents = agents

class Simulation(object):
    def __init__(self, graph, agents, workers, copy):
        self.graph = graph
        self.agents = agents
        self.workers = workers
        self.cost = 0
        if not copy:
            for agent in self.agents:
                if agent.pickup:
                    agent.path = AStar(self.graph, agent)
                    agent.walking_path = [agent.pos]

    def run(self):
        done = False
        while(not done):
            self.cost += 1
            for agent in self.agents:
                if not agent.pickup:
                    continue
                agent.one_step_in_path()

                if agent.done_with_target():
                    if not agent.pickup.advance_pickup_state(self.workers, agent.is_copy):
                        #Delivered back shelf
                        if not assign_item_to_agent(agent, self.workers):
                            agent.pickup = None
                            agent.is_carrying_shelf = False
                    if agent.pickup:
                        agent.is_carrying_shelf = agent.pickup.is_carrying_shelf()
                        agent.path = AStar(self.graph, agent)
                    else:
                        agent.path = []

            agent1, agent2 = self.agents_will_collide_next_step()
            if agent1:
                return State(agent1, agent2, self.agents), self.cost, done

            done = not one_agent_has_pickup(self.agents)

        return None, self.cost, done

    def one_iteration(self, p=False):
        done = False
        self.cost += 1
        for agent in self.agents:
            if not agent.pickup:
                continue
            agent.one_step_in_path()
            if p:
                print("agent%d just stepped and now has path" % (agent.id))
                print([x.id for x in agent.path])

            if agent.done_with_target():
                print("agent%d was done with target" % (agent.id))
                if not agent.pickup.advance_pickup_state(self.workers, agent.is_copy):
                    #Delivered back shelf
                    print("agent%d delivered back a SHELF" % (agent.id))
                    if not assign_item_to_agent(agent, self.workers):
                        agent.pickup = None
                        agent.is_carrying_shelf = False
                if agent.pickup:
                    print("agent%d STILL HAS A PICKUP" % (agent.id))
                    agent.is_carrying_shelf = agent.pickup.is_carrying_shelf()
                    print("agent %d is_carrying_shelf: %d" % (agent.id, agent.is_carrying_shelf))
                    agent.path = AStar(self.graph, agent, True)
                    print("agent %d new path is:" % (agent.id))
                    print([x.id for x in agent.path])
                else:
                    agent.path = []

        agent1, agent2 = self.agents_will_collide_next_step()
        if agent1:
            return State(agent1, agent2, self.agents), self.cost, done

        done = not one_agent_has_pickup(self.agents)

        return None, self.cost, done

    def agent_will_collide_next_step(self, agent):
        for j in range(0, len(self.agents)):
            other = self.agents[j]
            if agent.id == other.id:
                continue
            if len(agent.path) > 1 and len(other.path) > 1:
                #Regular collision
                if agent.path[1].id == other.path[1].id:
                    return agent, other

                #Swap collision
                if agent.path[0].id == other.path[1].id and agent.path[1].id == other.path[0].id:
                    return agent, other

        return None, None

    def agents_will_collide_next_step(self):
        for i in range(0, len(self.agents)):
            agent1 = self.agents[i]
            a1, a2 = self.agent_will_collide_next_step(agent1)
            if a1:
                return a1, a2
        return None, None

    def apply_rule(self, state, rule):
        if rule == 0:
            agent1 = self.find_correct_agent(state.agent1)
            return self.apply_swerve_rule(agent1)
        elif rule == 1:
            agent2 = self.find_correct_agent(state.agent2)
            return self.apply_swerve_rule(agent2)
        elif rule == 2:
            agent1 = self.find_correct_agent(state.agent1)
            return self.apply_wait_rule(agent1)
        elif rule == 3:
            agent2 = self.find_correct_agent(state.agent2)
            return self.apply_wait_rule(agent2)
        elif rule == 4:
            agent1 = self.find_correct_agent(state.agent1)
            agent2 = self.find_correct_agent(state.agent2)
            return self.apply_multi_swerve_rule(agent1, agent2)

    def find_correct_agent(self,copy_agent):
        for agent in self.agents:
            if agent.id == copy_agent.id:
                return agent
        print("Couldn't find copy_agent, wtf?")
        return None

    def apply_wait_rule(self, agent):
        agent.path.insert(0, agent.pos)
        t1, t2 = self.agent_will_collide_next_step(agent)
        if t1:
            return False
        return True

    def apply_swerve_rule(self, agent):
        neighbours = [(0,1),(1,0),(-1,0),(0,-1)]

        min_distance = 10**5
        min_neighbour = None
        for (i,j) in neighbours:
            x, y = (agent.pos.coordinates[0] + i, agent.pos.coordinates[1] + j)
            if x < 0 or x >= self.graph.shape[0] or y < 0 or y >= self.graph.shape[1]:
                # neighbour coordinates are out of the graph
                continue
            neighbour = self.graph[x][y]
            if neighbour.type == NodeType.OBSTACLE:
                #print("can't swevre to %d bcause OBSTACLE" % (neighbour.id))
                continue

            agent.path = [agent.pos, neighbour]
            a1, a2 = self.agent_will_collide_next_step(agent)
            if a1:
                #print("can't swevre to %d bcause will collide next" % (neighbour.id))
                continue

            new_distance = manhattan_distance(neighbour, agent.pickup.get_target())
            if new_distance < min_distance:
                min_neighbour = neighbour
                min_distance = new_distance

        if min_neighbour:
            temp_pos = agent.pos
            agent.pos = min_neighbour
            agent.path = AStar(self.graph, agent)
            agent.path.insert(0, temp_pos)
            agent.pos = temp_pos
            return True
        return False

    def apply_multi_swerve_rule(self, agent1, agent2):
        neighbours = [(0,1),(1,0),(-1,0),(0,-1)]

        min_distance = 10**5
        min_neighbour1 = None
        min_neighbour2 = None
        for (i,j) in neighbours:
            x, y = (agent1.pos.coordinates[0] + i, agent1.pos.coordinates[1] + j)

            if x < 0 or x >= self.graph.shape[0] or y < 0 or y >= self.graph.shape[1]:
                # neighbour coordinates are out of the graph
                continue

            neighbour1 = self.graph[x][y]
            if neighbour1.type == NodeType.OBSTACLE:
                continue

            for (k,l) in neighbours:
                a, b = (agent2.pos.coordinates[0] + k, agent2.pos.coordinates[1] + l)

                if a < 0 or a >= self.graph.shape[0] or b < 0 or b >= self.graph.shape[1]:
                    # neighbour coordinates are out of the graph
                    continue

                neighbour2 = self.graph[a][b]
                if neighbour2.type == NodeType.OBSTACLE:
                    continue

                agent1.path = [agent1.pos, neighbour1]
                agent2.path = [agent2.pos, neighbour2]

                t1, t2 = self.agent_will_collide_next_step(agent1)
                t3, t4 = self.agent_will_collide_next_step(agent2)
                if t1 or t3:
                    continue

                new_distance = manhattan_distance(neighbour1, agent1.pickup.get_target())
                new_distance += manhattan_distance(neighbour2, agent2.pickup.get_target())
                if new_distance < min_distance:
                    min_neighbour1 = neighbour1
                    min_neighbour2 = neighbour2
                    min_distance = new_distance

        if min_neighbour1:
            temp_pos1 = agent1.pos
            agent1.pos = min_neighbour1
            agent1.path = AStar(self.graph, agent1)
            agent1.path.insert(0, temp_pos1)
            agent1.pos = temp_pos1

            temp_pos2 = agent2.pos
            agent2.pos = min_neighbour2
            agent2.path = AStar(self.graph, agent2)
            agent2.path.insert(0, temp_pos2)
            agent2.pos = temp_pos2
            return True
        return False
