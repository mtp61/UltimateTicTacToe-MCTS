
public class Client {
	public static final int MAX_TIME = 5;
	
	public static void main(String args[]) {
		// make the game and the bot and the shared class
		Game game = new Game();
		Bot bot = new Bot(MAX_TIME);
		
		// draw starting board
		System.out.println("Ultimate Tic-Tac-Toe");
		game.drawBoard();
		
		// main loop
		int current_player = 1;
		while (true) {
			if (current_player == 1) {
				// get player move
				game.playerMove();
				
				// next player is up
				current_player = 2;
			} else {
				// get bot move
				game.botMove(bot);
				
				// next player is up
				current_player = 1;
			}
			
			game.drawBoard();

			// check for win
			int win_status = Shared.checkWin(game.getBigBoard());
			if (win_status == 1) {
				System.out.println("Player win");
			} else if (win_status == 2) {
				System.out.println("Bot win");
			} else if (win_status == -1) {
				System.out.println("Draw");
			}
		}
	}
}
