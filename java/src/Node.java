import java.util.LinkedList;
import java.util.Random;

public class Node {
	private static final char[] ROW_LABELS = {'1', '2', '3', '4', '5', '6', '7', '8', '9'};
	private static final char[] COLUMN_LABELS = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'};
		
	private int[] board;
	private int[] big_board;
	private int next_subgame;
	private int move;
	private int player_to_act;
	private int is_win;
	
	private LinkedList<Node> children = new LinkedList<Node>();
	private int num_visits = 0;
	private int sim_outcomes_1 = 0;
	private int sim_outcomes_2 = 0;
	private int sim_outcomes_m1 = 0;
	
	private String id;
	
	private Random rand = new Random(System.currentTimeMillis());
	
	public Node(int[] board, int[] big_board, int next_subgame, int move, int player_to_act, String id) {
		// game state info
		this.board = board;
		this.big_board = big_board;
		this.next_subgame = next_subgame;
		this.move = move;
		this.player_to_act = player_to_act;
		this.is_win = Shared.checkWin(big_board);
		
		this.id = id;
	}
	
	public Node(int[] board, int[] big_board, int next_subgame, int move, int player_to_act) {
		// game state info
		this.board = board;
		this.big_board = big_board;
		this.next_subgame = next_subgame;
		this.move = move;
		this.player_to_act = player_to_act;
		this.is_win = Shared.checkWin(big_board);
		
		this.id = "node";
	}
	
	public void generateChildren() {
		// make sure we need to do this
		if (this.children.size() == 0) {
			// get potential moves
			LinkedList<Integer> potential_moves = new LinkedList<Integer>();
			if (this.next_subgame == -1) {
				// need to check all squares
				for (int i = 0; i < 81; i++) {
					if (this.board[i] == 0) {
						potential_moves.add(i);
					}
				}
			} else {
				// just need to check subgame squares
				for (int i = 9 * this.next_subgame; i < 9 * this.next_subgame + 9; i++) {
					if (this.board[i] == 0) {
						potential_moves.add(i);
					}
				}
			}
						
			// make a child for each of the potential moves
			for (int i = 0; i < potential_moves.size(); i++) {
				int[] new_board = new int[81];
				for (int j = 0; j < 81; j++) {
					new_board[j] = this.board[j];
				}
				new_board[potential_moves.get(i)] = this.player_to_act;
				
				int col_index = (potential_moves.get(i) % 3 + 3 * ((int) (potential_moves.get(i) / 9) % 3)) % 9;
				int row_index = ((int) (potential_moves.get(i) / 3) % 3 + 3 * (int) (potential_moves.get(i) / 27)) % 9;
				String new_id = String.valueOf(Node.COLUMN_LABELS[col_index]) + String.valueOf(Node.ROW_LABELS[row_index]);
				
				int[] new_big_board = new int[9];
				for (int j = 0; j < 9; j++) {
					new_big_board[j] = this.big_board[j];
				}
				BoardObj board_obj = Shared.updateBigBoard(new_board, new_big_board, potential_moves.get(i));
				new_board = board_obj.board;
				new_big_board = board_obj.big_board;
				int new_next_subgame;
				if (new_big_board[potential_moves.get(i) % 9] == 0) {
					new_next_subgame = potential_moves.get(i) % 9;
				} else {
					new_next_subgame = -1;
				}
				int new_player_to_act;
				if (this.player_to_act == 1) {
					new_player_to_act = 2;
				} else {
					new_player_to_act = 1;
				}
				this.children.add(new Node(new_board, new_big_board, new_next_subgame, potential_moves.get(i), new_player_to_act, new_id));
			}
		}
	}
	
	public int simulateGame() {
		// need to deep copy node
		Node current_node = new Node(this.board, this.big_board, this.next_subgame, this.move, this.player_to_act, this.id);
		
		// loop until game over
		while (current_node.getIsWin() == 0) {
			// get children
			current_node.generateChildren();
			
			// pick random child
			int num_children = current_node.getChildren().size();
			current_node = current_node.getChildren().get(rand.nextInt(num_children));
		}
		
		return current_node.getIsWin();
	}

	public int getNumVisits() {
		return this.num_visits;
	}

	public LinkedList<Node> getChildren() {
		return this.children;
	}

	public void incrementVisits() {
		this.num_visits++;		
	}

	public void incrementSim1() {
		this.sim_outcomes_1++;		
	}
	
	public void incrementSim2() {
		this.sim_outcomes_2++;		
	}
	
	public void incrementSimM1() {
		this.sim_outcomes_m1++;		
	}

	public int getIsWin() {
		return this.is_win;
	}
	
	public int getSimOutcomes1() {
		return sim_outcomes_1;
	}
	
	public int getSimOutcomes2() {
		return sim_outcomes_2;
	}
	
	public int getSimOutcomesM1() {
		return sim_outcomes_m1;
	}
	
	public int getMove() {
		return this.move;
	}

	public String getId() {
		return this.id;
	}

	public int getPlayerToAct() {
		return this.player_to_act;
	}	
}
