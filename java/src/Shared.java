
public class Shared {	
	public static int linesToBoard(int move_lines) {
		int col_index = move_lines % 9;
		int row_index = (int) (move_lines / 9);
		
		return col_index % 3 + 9 * (int) (col_index / 3) + 3 * (row_index % 3) + 27 * (int) (row_index / 3);
	}
	
	public static int checkWin(int[] board) {
		// check for win
		// check rows
		for (int i = 0; i < 3; i++) {
			int row_sum = 0;
			int num_filled = 0;
			for (int j = 0; j < 3; j++) {
				row_sum += board[3 * i + j];
				if (board[3 * i + j] != 0 && board[3 * i + j] != -1) {
	                num_filled++;
				}
			}
			if (num_filled == 3) {
	            if (row_sum == 3) {
	                return 1;
	            } else if (row_sum == 6) {
	                return 2;
	            }
			}
		}
		
		// check cols
		for (int i = 0; i < 3; i++) {
			int col_sum = 0;
			int num_filled = 0;
			for (int j = 0; j < 3; j++) {
				col_sum += board[i + 3 * j];
				if (board[3 * i + j] != 0 && board[i + 3 * j] != -1) {
	                num_filled++;
				}
			}
			if (num_filled == 3) {
	            if (col_sum == 3) {
	                return 1;
	            } else if (col_sum == 6) {
	                return 2;
	            }
			}
		}
		
		// check diagonals
	    if (board[0] != 0 && board[4] != 0 && board[8] != 0 && board[0] != -1 && board[4] != -1 && board[8] != -1) {
			int diag_sum = board[0] + board[4] + board[8];
	    	if (diag_sum == 3) {
	            return 1;
	        } else if (diag_sum == 6) {
	            return 2;
	        }
	    }
	    if (board[2] != 0 && board[4] != 0 && board[6] != 0 && board[2] != -1 && board[4] != -1 && board[6] != -1) {
	        int diag_sum = board[2] + board[4] + board[6];
	        if (diag_sum == 3) {
	            return 1;
	    	} else if (diag_sum == 6) {
	            return 2;
	    	}
	    }
	
	    // check if board full
	    int open_squares = 0;
	    for (int i = 0; i < 9; i++) {
	        if (board[i] == 0) {
	            open_squares++;
	        }
	    }
	    if (open_squares == 0) {
	        return -1;
	    }
	
	    // return not win or tie
	    return 0;
	}
	
	public static BoardObj updateBigBoard(int[] board, int[] big_board, int move) {
		int subgame = (int) (move / 9);
		int[] subgame_board = new int[9];
		for (int i = 0; i < 9; i++) {
			subgame_board[i] = board[9 * subgame + i];
		}
			    
	    int win_result = Shared.checkWin(subgame_board);
	    if (win_result != 0) {
	        big_board[subgame] = win_result;
	        if (win_result == 1) {
	            for (int i = 9 * subgame; i < 9 * subgame + 9; i++) {
	                board[i] = 1;
	            }
	        } else if (win_result == 2) {
	        	for (int i = 9 * subgame; i < 9 * subgame + 9; i++) {
	                board[i] = 2;
	            }
	        }
	    }
	
		return new BoardObj(board, big_board);
	}
}
