import java.util.Scanner;

public class Game {
	private static final char[] ROW_LABELS = {'1', '2', '3', '4', '5', '6', '7', '8', '9'};
	private static final char[] COLUMN_LABELS = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'};
	
	private int[] board = new int[81];
	private int[] big_board = new int[9];
	
	private int next_subgame = -1;
	
	private Scanner scanner = new Scanner(System.in);
	
	public Game() {
		for (int i = 0; i < 81; i++) {
			board[i] = 0;
		}
		for (int i = 0; i < 9; i++) {
			big_board[i] = 0;
		}
	}
	
	public void drawBoard() {
		System.out.println();
		
		for (int i = 0; i < 9; i++) {
			System.out.print(" " + this.ROW_LABELS[i] + " ");
			for (int j = 0; j < 9; j++) {
				switch (this.board[Shared.linesToBoard(9 * i + j)]) {
				case 0:
					System.out.print(" ");
					break;
				case 1:
					System.out.print("X");
					break;
				case 2:
					System.out.print("O");
					break;
				}
				
				if ((j + 1) % 3 != 0) {
					System.out.print(" ");
				} else if (j != 8) {
					System.out.print("|");
				}
			}
			System.out.println();
			
			if ((i + 1) % 3 == 0 && i != 8) {
				System.out.println("   -----|-----|-----");
			}
		}
		System.out.println();
		System.out.print("  ");
		
		for (int j = 0; j < 9; j++) {
			System.out.print(this.COLUMN_LABELS[j] + " ");
		}
		
		System.out.println();
	}
	
	public void playerMove() {
		// make the vars for telling the user which subgame to play in
		char col_low, col_high, row_low, row_high;
		if (this.next_subgame == -1) {
			col_low = 'a';
		    col_high = 'i';
            row_low = '1';
            row_high = '9';
		} else {
			col_low = Game.COLUMN_LABELS[3 * (this.next_subgame % 3)];
            col_high = Game.COLUMN_LABELS[3 * (this.next_subgame % 3) + 2];
            row_low = Game.ROW_LABELS[3 * (int) (this.next_subgame / 3)];
            row_high = Game.ROW_LABELS[3 * (int) (this.next_subgame / 3) + 2];
		}
		
		// loop until we have a valid move
		int move_parsed = 0;
		while (true) {
			System.out.print("Enter your move [" + col_low + "-" + col_high + "][" + row_low + "-" + row_high + "]: ");
			String move = scanner.nextLine();
			
			// check that move follows format
			if (move.length() != 2) {
				continue;
			}
			boolean col_contains = false;
			boolean row_contains = false;
			int col_index = 0;
			int row_index = 0;
			for (int i = 0; i < 9; i++) {
				if (Game.COLUMN_LABELS[i] == move.charAt(0)) {
					col_contains = true;
					col_index = i;
				}
			}
			for (int i = 0; i < 9; i++) {
				if (Game.ROW_LABELS[i] == move.charAt(1)) {
					row_contains = true;
					row_index = i;
				}
			}
			if (!(col_contains && row_contains)) {
				continue;
			}
			
			// check that move is legal
			move_parsed = Shared.linesToBoard(9 * row_index + col_index);
			
			// check correct subgame
			if (this.next_subgame != -1) {
				if ((int) (move_parsed / 9) != this.next_subgame) {
					continue;
				}
			}
			
			// check open square
			if (this.board[move_parsed] != 0) {
				continue;
			}
			
			// if we get to here in the loop the move is valid
			break;
		}
		
		// execute the move
		this.board[move_parsed] = 1;
		
		// update big board
		BoardObj board_obj = Shared.updateBigBoard(this.board, this.big_board, move_parsed);
		this.board = board_obj.board;
		this.big_board = board_obj.big_board;
		
		// update next subgame
		if (this.big_board[move_parsed % 9] == 0) {
			this.next_subgame = move_parsed % 9;
		} else {
			this.next_subgame = -1;
		}
	}
		
		
	
	public void botMove(Bot bot) {
		// get move
		int move = bot.getMove(this.board, this.big_board, this.next_subgame);
		
		// execute the move
		this.board[move] = 2;
		
		// update big board
		BoardObj board_obj = Shared.updateBigBoard(this.board, this.big_board, move);
		
		this.board = board_obj.board;
		this.big_board = board_obj.big_board;
		
		
		// update next subgame
		if (this.big_board[move % 9] == 0) {
			this.next_subgame = move % 9;
		} else {
			this.next_subgame = -1;
		}
	}
	
	public int[] getBigBoard() {
		return this.big_board;
	}
}
