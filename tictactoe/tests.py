import unittest

from tictactoe import initial_state, terminal, winner, player, actions, result, min_value, max_value, minimax

class Tests(unittest.TestCase):

	def test_1(self):
		"""Check Terminal"""
		return self.assertFalse(terminal(initial_state()))

	def test_2(self):
		"""Check winner function for None"""
		return self.assertEqual(winner([[None, None, None],[None, None, None],[None, None, None]]), None)

	def test_3(self):
		"""Check winner function for "X" """
		return self.assertEqual(winner([["X", None, None],[None, "X", None],[None, None, "X"]]), "X")

	def test_4(self):
		"""Check winner function for O """
		return self.assertEqual(winner([["O","X","O"],["O","X","X"],["X","O","X"]]), None)

	def test_9(self):
		"""Check winner function for tie """
		return self.assertEqual(winner([["O", "O", "O"],[None, "X", None],["O", "X", None]]), "O")

	def test_5(self):
		"""CHeck turn functions"""
		return self.assertEqual(player([[None, None, None],[None, None, None],[None, None, None]]), "X")

	def test_6(self):
		"""Check turn function for O"""
		return self.assertEqual(player([["X", None, None],[None,None,None],[None,None,None]]),"O")

	def test_7(self):
		"""Player Function for X"""
		return self.assertEqual(player([["X","O",None],[None,"X","O"],[None,None,None]]),"X")

	def test_8(self):
		"""player function if game is over"""
		return self.assertEqual(player([["O","X","O"],["O","X","X"],["X","O","X"]]),None)

	def test_10(self):
		"""ACtions test"""
		return self.assertEqual(actions([["O","X",None],["O",None,"X"],["X","O","X"]]), {(0,2),(1,1)})
	def test_11(self):
		"""result test"""
		return self.assertEqual(result([[None, None, None],[None, None, None],[None, None, None]],(0,1)),[[None, "X", None],[None, None, None],[None, None, None]])
	def test_12(self):
		"""terminal test"""
		return self.assertEqual(terminal([["O", "O", "O"],[None, "X", None],["O", "X", None]]),True)

	def test_13(self):
		"""Terminal test part 2"""
		return  self.assertEqual(terminal([["O","X","O"],["O","X","X"],["X","O","X"]]),True)

	def test_14(self):
		"""Terminal test part 3"""
		return self.assertTrue(terminal([["X", None, None],[None, "X", None],[None, None, "X"]]))

	def test_15(self):
		"""Test max_value"""
		return self.assertEqual(max_value([["X", None, None],[None, "X", None],[None, None, None]])[0],1)

	def test_16(self):
		"""Test max_value"""
		return self.assertEqual(max_value([["O","X","O"],["O","X","X"],["X","O",None]])[0],0)

	def test_17(self):
		"""Test min_value"""
		return self.assertEqual(min_value([["O", None, None],[None, "O", None],[None, None, None]])[0],-1)

	def test_18(self):
		"""Test min_value"""
		return self.assertEqual(min_value([[None,"X","O"],["O","X","X"],["X",None,"O"]])[0],0)

	def test_19(self):
		"""Test max_value, move"""
		return self.assertEqual(min_value([[None,"X","O"],["O","X","X"],["X",None,"O"]])[1],(2,1))

	def test_20(self):
		return self.assertEqual(minimax(initial_state()), (0,1))

if __name__ == "__main__":
	unittest.main()







