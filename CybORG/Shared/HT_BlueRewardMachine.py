
from CybORG.Shared.RewardCalculator import RewardCalculator
from CybORG.Simulator.State import State
from CybORG.Simulator.Actions.GreenActions import GreenAccessService, GreenLocalWork
from CybORG.Simulator.Actions.AbstractActions.ExploitRemoteService import ExploitRemoteService
from CybORG.Simulator.Actions.AbstractActions.PrivilegeEscalate import PrivilegeEscalate
from CybORG.Simulator.Actions.AbstractActions.Impact import Impact

from CybORG.Simulator.Actions.Action import InvalidAction

class HT_BlueRewardMachine(RewardCalculator):
    """The reward calculator for HTScenario

    """
    def calculate_reward(self, current_state: dict, action_dict: dict, agent_observations: dict, done: bool, state: State):
        """Calculate the cumulative reward.

        Parameters
        ----------
        current_state : Dict[str, _]
            the current state of all the hosts in the simulation
        action_dict : dict
        agent_observations : Dict[str, ObservationSet]
            current agent observations
        done : bool
            has the episode ended
        state: Statek
            current State object

        Returns
        -------
        : int
            sum of the rewards collected
        """
        rewards = {
            "LSsub" : {"REX":-3, "RPE":-5, "RIM":-10},
            "LCsub" : {"REX":-2, "RPE":-4, "RIM":-8},
            "LSsub" : {"REX":-1, "RPE":-3, "RIM":-6},
            "LSsub" : {"REX":-5, "RPE":-7, "RIM":-10},
        }
        reward_list = []

        for agent_name, action in action_dict.items():
            if not action:
                continue
            
            action = action[0]            
            if isinstance(action, (Impact, PrivilegeEscalate)):
                hostname = action.hostname
            elif isinstance(action, ExploitRemoteService):
                hostname = state.ip_addresses[action.ip_address]
            else:
                continue

            subnet_name = state.hostname_subnet_map[hostname].value
            sessions = state.sessions[agent_name].values()

            #设备类型对奖励的影响
            if "user" in hostname:
                delta = 0.5
            elif "server" in hostname:
                delta = -0.5

            if len([session.ident for session in sessions if session.active]) > 0:
                success = agent_observations[agent_name].observations[0].data['success']
                rewards_for_zone = rewards[subnet_name]

                #每轮统计奖励
                if 'red' in agent_name and success:
                    if isinstance(action, Impact):
                        reward_list.append(rewards_for_zone["RIM"]+delta)
                    elif isinstance(action, PrivilegeEscalate):
                        reward_list.append(rewards_for_zone["RPE"]+delta)
                    elif isinstance(action, ExploitRemoteService):
                        reward_list.append(rewards_for_zone["REX"]+delta)


        return sum(reward_list)


  
        
        
 
     
        
    