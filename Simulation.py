from AStar import *
from functions import *
import copy

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
            for agent in self.agents:
                if not agent.pickup:
                    continue
                agent.one_step_in_path()
                self.cost += 1
                if agent.done_with_target():
                    if not agent.pickup.advance_pickup_state(self.workers, agent.is_copy):
                        x,y = agent.pickup.target_list[0].coordinates
                        self.graph[x][y].booked = False
                        #Delivered back shelf
                        if not assign_item_to_agent(agent, self.workers):
                            agent.pickup = None
                            agent.is_carrying_shelf = False
                    if agent.pickup:
                        x,y = agent.pickup.target_list[0].coordinates
                        self.graph[x][y].booked = True
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
                if p:
                    print("agent%d was done with target" % (agent.id))
                if not agent.pickup.advance_pickup_state(self.workers, agent.is_copy):
                    x,y = agent.pickup.target_list[0].coordinates
                    self.graph[x][y].booked = False
                    #Delivered back shelf
                    if p:
                        print("agent%d delivered back a SHELF" % (agent.id))
                    if not assign_item_to_agent(agent, self.workers):
                        agent.pickup = None
                        agent.is_carrying_shelf = False
                if agent.pickup:
                    x,y = agent.pickup.target_list[0].coordinates
                    self.graph[x][y].booked = True
                    if p:
                        print("agent%d STILL HAS A PICKUP" % (agent.id))
                    agent.is_carrying_shelf = agent.pickup.is_carrying_shelf()
                    if p:
                        print("agent %d is_carrying_shelf: %d" % (agent.id, agent.is_carrying_shelf))
                    agent.path = AStar(self.graph, agent, p)
                    if p:
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
                if agent.path[1].id == other.path[1].id and agent.path[1].type != NodeType.DROPOFF:
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

    def can_apply_rule(self, state, rule):
        agent1_old_path = state.agent1.path.copy()
        agent2_old_path = state.agent2.path.copy()
        if rule == 0:
            ok, new_path = self.apply_swerve_rule(state.agent1, state.agent2)
            state.agent1.path = agent1_old_path
            state.agent2.path = agent2_old_path
            return ok, new_path, None
        elif rule == 1:
            ok, new_path = self.apply_swerve_rule(state.agent2, state.agent1)
            state.agent1.path = agent1_old_path
            state.agent2.path = agent2_old_path
            return ok, None, new_path
        elif rule == 2:
            ok, new_path = self.apply_wait_rule(state.agent1, state.agent2)
            state.agent1.path = agent1_old_path
            state.agent2.path = agent2_old_path
            return ok, new_path, None
        elif rule == 3:
            ok, new_path = self.apply_wait_rule(state.agent2, state.agent2)
            state.agent1.path = agent1_old_path
            state.agent2.path = agent2_old_path
            return ok, None, new_path
        elif rule == 4:
            ok, new_path1, new_path2 = self.apply_multi_swerve_rule(state.agent1, state.agent2)
            state.agent1.path = agent1_old_path
            state.agent2.path = agent2_old_path
            # if ok:
            #     print("found new paths")
            #     print([x.id for x in new_path1])
            #     print([x.id for x in new_path2])
            #     print("old paths")
            #     print([x.id for x in state.agent1.path])
            #     print([x.id for x in state.agent2.path])
            return ok, new_path1, new_path2

    def apply_rule(self, state, rule, new_path1, new_path2):
        if rule == 0:
            agent1 = self.find_correct_agent(state.agent1)
            agent1.path = new_path1
            return
        elif rule == 1:
            agent2 = self.find_correct_agent(state.agent2)
            agent2.path = new_path2
            return
        elif rule == 2:
            agent1 = self.find_correct_agent(state.agent1)
            agent1.path = new_path1
            return
        elif rule == 3:
            agent2 = self.find_correct_agent(state.agent2)
            agent2.path = new_path2
            return
        elif rule == 4:
            agent1 = self.find_correct_agent(state.agent1)
            agent2 = self.find_correct_agent(state.agent2)
            agent1.path = new_path1
            agent2.path = new_path2
            return

    def find_correct_agent(self,copy_agent):
        for agent in self.agents:
            if agent.id == copy_agent.id:
                return agent
        print("Couldn't find copy_agent, wtf?")
        return None

    def apply_swerve_rule(self, agent_to_swerve, other_agent):
        max_reserve = 3
        if len(other_agent.path) < 3:
            max_reserve = len(other_agent.path)
        reservation_table = [(x.id, index) for index,x in enumerate(other_agent.path[:max_reserve])]
        new_path = AStarReserved(self.graph, agent_to_swerve, reservation_table)
        if new_path:
            agent_to_swerve.path = new_path
            return True, new_path
        return False, None

    def apply_wait_rule(self, agent_to_wait, other_agent):
        agent_to_wait.path.insert(0, agent_to_wait.pos)
        t1, t2 = self.agent_will_collide_next_step(agent_to_wait)
        if t1:
            return False, None
        return True, agent_to_wait.path.copy()

    def all_other_agent_reserved(self, id1, id2):
        list = []
        for a in self.agents:
            if a.id == id1 or a.id == id2:
                continue
            max_reserve = 4
            if len(a.path) < 4:
                max_reserve = len(a.path)
            list += [(x.id, index) for index, x in enumerate(a.path[:max_reserve])]
        return list

    def one_agent_prio(self, prio_agent, other_agent, prio_agent_col_node, other_agent_col_node):
        reservation_table = [prio_agent_col_node] + self.all_other_agent_reserved(prio_agent.id, other_agent.id)
        prio_agent_new_path = AStarReserved(self.graph, prio_agent, reservation_table)

        if not prio_agent_new_path:
            # couldnt find any path
            return False, None, None

        max_reserve = 4
        if len(prio_agent_new_path) < 4:
            max_reserve = len(prio_agent_new_path)
        reservation_table = [(x.id, index) for index, x in enumerate(prio_agent_new_path[:max_reserve])]
        reservation_table.append(other_agent_col_node)
        reservation_table += self.all_other_agent_reserved(prio_agent.id, other_agent.id)
        other_agent_new_path = AStarReserved(self.graph, other_agent, reservation_table)

        if not other_agent_new_path:
            # couldnt find any path
            return False, None, None

        return True, prio_agent_new_path, other_agent_new_path


    def apply_multi_swerve_rule(self, agent1, agent2, old=False):
        agent1_collision_node = (agent1.path[1].id, 1)
        agent2_collision_node = (agent2.path[1].id, 1)

        worked, p1, p2 = self.one_agent_prio(agent1, agent2, agent1_collision_node, agent2_collision_node)

        cost1 = -1
        if worked:
            cost = len(p1) + len(p2)

        worked2, p3, p4 = self.one_agent_prio(agent2, agent1, agent2_collision_node, agent1_collision_node)

        if not worked2 and cost1 == -1:
            return False, None, None
        if not worked2:
            # print("found")
            # print("p1: ")
            # print([x.id for x in p1])
            # print("p2: ")
            # print([x.id for x in p2])
            return True, p1, p2

        if worked2 and cost1 == -1:
            # print("found")
            # print("p4: ")
            # print([x.id for x in p4])
            # print("p3: ")
            # print([x.id for x in p3])
            return True, p4, p3


        cost2 = len(p3) + len(p4)
        if cost2 < cost1:
            # print("found")
            # print("p4: ")
            # print([x.id for x in p4])
            # print("p3: ")
            # print([x.id for x in p3])
            return True, p4, p3
        else:
            # print("found")
            # print("p4: ")
            # print([x.id for x in p4])
            # print("p3: ")
            # print([x.id for x in p3])
            return True, p1, p2
