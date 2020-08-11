import java.util.HashSet;
import java.util.LinkedList;
import java.util.Set;

public class Bot {
	private int MAX_TIME;
	
	public Bot(int MAX_TIME) {
		this.MAX_TIME = MAX_TIME;
	}
	
	public int getMove(int[] board, int[] big_board, int next_subgame) {
		// get start time
		int start_time = (int) (System.currentTimeMillis() / 1000);
		
		// make the root node
		Node root = new Node(board, big_board, next_subgame, -1, 2, "root");
		root.generateChildren();
		
		int nodes_searched = 0;
		while ((System.currentTimeMillis() / 1000) - start_time < this.MAX_TIME) { // loop until out of time
			// selection
			Node current_node = root;
			LinkedList<Node> node_chain = new LinkedList<Node>();
			node_chain.add(root);
			
			// for dfs in choosing a node
			Set<Node> visited = new HashSet<Node>();
			visited.add(root);
			
			// keep searching until we have a node with no visits
			while (current_node.getNumVisits() > 0 || current_node.equals(root)) {
				// check children
				LinkedList<Node> non_visited_children = new LinkedList<Node>();
				for (int i = 0; i < current_node.getChildren().size(); i++) {
					if (!visited.contains(current_node.getChildren().get(i))) {
						non_visited_children.add(current_node.getChildren().get(i));
					}
				}
				
				if (non_visited_children.size() > 0) {
					// pick a child
					double max_score = -1;
					Node max_child = null;
					for (int i = 0; i < non_visited_children.size(); i++) {
						if (non_visited_children.get(i).getNumVisits() == 0) {
							// select child
							max_child = non_visited_children.get(i);
							break;
						}
						
						int parent_player = current_node.getPlayerToAct();
						double num_wins;
						if (parent_player == 1) {
							num_wins = non_visited_children.get(i).getSimOutcomes1() + 0.5 * non_visited_children.get(i).getSimOutcomesM1();
						} else {
							num_wins = non_visited_children.get(i).getSimOutcomes2() + 0.5 * non_visited_children.get(i).getSimOutcomesM1();
						}
						double win_ratio = num_wins / non_visited_children.get(i).getNumVisits();
						
						int parent_visits = current_node.getNumVisits();
						double explore_component = Math.sqrt(2 * Math.log(parent_visits) / non_visited_children.get(i).getNumVisits());
						
						double child_score = win_ratio + explore_component;
						
						if (child_score > max_score) {
							max_score = child_score;
							max_child = non_visited_children.get(i);
						}
					}
					
					current_node = max_child;
					node_chain.add(current_node);
				} else {
					// if at root
					if (current_node.equals(root)) {
						// tree is complete
						break;
					}
					
					// go up the chain
					node_chain.remove(node_chain.size() - 1);
					current_node = node_chain.get(node_chain.size() - 1);
					
				}
				
				// check if tree complete
				if (current_node.equals(root)) {
					System.out.println("tree complete");
					break;
				}
				
				// expansion
				current_node.generateChildren();
				
				// simulation
				int simulation_result = current_node.simulateGame();
				
				// backpropogation
				for (int i = 0; i < node_chain.size(); i++) {
					node_chain.get(i).incrementVisits();
					if (simulation_result == 1) {
						node_chain.get(i).incrementSim1();
					} else if (simulation_result == 2) {
						node_chain.get(i).incrementSim2();
					} else if (simulation_result == -1) {
						node_chain.get(i).incrementSimM1();
					}
				}
			}
						
			nodes_searched++;
		}
				
		// find the best move
		double best_child_score = -2;
		Node best_child_node = null;
		for (int i = 0; i < root.getChildren().size(); i++ ) {
			double child_score;
			if (root.getChildren().get(i).getIsWin() == 2) {
				// pick the move, don't need to do anything else
				best_child_node = root.getChildren().get(i);
				break;
			} else if (root.getChildren().get(i).getIsWin() == 1) {
				child_score = -1;
			} else if (root.getChildren().get(i).getIsWin() == -1) {
				child_score = 0;
			} else {
				child_score = (root.getChildren().get(i).getSimOutcomes2() + 0.5 * root.getChildren().get(i).getSimOutcomesM1()) / root.getChildren().get(i).getNumVisits();
			}
			
			if (child_score > best_child_score) {
				best_child_node = root.getChildren().get(i);
				best_child_score = child_score;
			}
		}
				
		// output move
		System.out.println("bot played " + best_child_node.getId() + ", result of searching " + nodes_searched + " nodes");
		
		return best_child_node.getMove();
	}
}
