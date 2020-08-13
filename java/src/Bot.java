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
		long start_time = System.currentTimeMillis();
		
		// make the root node
		Node root = new Node(board, big_board, next_subgame, -1, 2, "root");
		root.generateChildren();
		
		int nodes_searched = 0;
		while (System.currentTimeMillis() - start_time < 1000 * this.MAX_TIME) { // loop until out of time		
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
				
				if (!visited.contains(current_node)) {
					visited.add(current_node);
				}

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
		
		// draw tree
		this.drawTree(root, 0, false);
		
		// output move
		System.out.println("bot played " + best_child_node.getId() + ", result of searching " + nodes_searched + " nodes");
		
		return best_child_node.getMove();
	}
	
	private void drawTree(Node root, int max_depth, boolean show_no_visit_nodes) {
		System.out.println();
		
		// make the stack
		LinkedList<NodeObj> node_stack = new LinkedList<NodeObj>();
		node_stack.add(new NodeObj(root, 0));
		
		// dfs until stack empty
		NodeObj top_node_obj;
		Node top_node;
		int depth;
		while (node_stack.size() > 0) {
			// get top node
			top_node_obj = node_stack.get(node_stack.size() - 1);
			node_stack.remove(node_stack.size() - 1);
			top_node = top_node_obj.node;
			depth = top_node_obj.depth;

			if (show_no_visit_nodes || top_node.getNumVisits() > 0) {  // should draw
				if (depth <= max_depth) {
					if (depth != 0) {
						String output = "";
						for (int i = 0; i < depth - 1; i++) {
							output += "    ";
						}
						System.out.print(output + "----");
					}
					
					int parent_player_to_act;
					if (top_node.getPlayerToAct() == 1) {
						parent_player_to_act = 2;
					} else {
						parent_player_to_act = 1;
					}
					
					if (top_node.getIsWin() != 0) {
						System.out.println(String.valueOf(parent_player_to_act) + " " + top_node.getId() + ": finished " + String.valueOf(top_node.getIsWin()));
					} else {
						// format is win loss tie / visits from the bots perspective
						System.out.println(String.valueOf(parent_player_to_act) + " " + top_node.getId() + ": " + 
						String.valueOf(top_node.getSimOutcomes2()) + " " + String.valueOf(top_node.getSimOutcomes1()) + " " + 
						String.valueOf(top_node.getSimOutcomesM1()) + " / " + String.valueOf(top_node.getNumVisits()));
					}
				}
				
				
			}
			
			// add children to stack
			for (int i = 0; i < top_node.getChildren().size(); i++) {
				node_stack.add(new NodeObj(top_node.getChildren().get(i), depth + 1));
			}
		}
		
		// add a newline
		System.out.println();
	}
}
