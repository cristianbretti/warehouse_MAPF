
class state:
    colAgent1pos = (x,y)
    colAgent2pos = (x,y)
    other_Agetnst_pos = [(x,y),(x,y)]

class Node:
    state = New STATE
    cost = int
    chil1 = None
    chil2 = None
    chil3 = None


class simulation:
    graph
    agents
    workers

    def run():
        bool done = False
        while(not done):
            for a in agent:
                a.step_one
                if a.pos == target:
                    change_target_fuck with pickup
                    plan_new_path_for_a

            a1, a2 = agents_will_collide_next_step():
            if a1 and a2:
                return new State(), cost, done

            done = not one_agent_no_pickup()

        return None, this.cost, done

    def apply_rule(int rule):
        move_agents_according_to_rule(rule)
        plan_new_paths()



rule_expert(node)
    bool done = False
    node.state, node.cost, done = node.simulation.run()

    if done:
        return


    child1.simulation = deepcopy(simulation)
    child2.simulation = deepcopy(simulation)
    child3.simulation = deepcopy(simulation)

    child1.simulation.apply_rule(1)
    child2.simulation.apply_rule(2)
    child3.simulation.apply_rule(3)

    node.child1 = child1
    node.child2 = child2
    node.child3 = child3

    rule_expert(child1)
    rule_expert(child2)
    rule_expert(child3)
