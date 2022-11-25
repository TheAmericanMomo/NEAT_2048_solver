import pygame
from Source import Game
import neat
import os
import pickle

class NEATGame:
    def __init__(self,list, window, width, height, header_size):
        self.game = Game(list, window, width, height, header_size)

    """
    This function allows a user to play the game
    """
    def play_game(self):
        self.game.board.generate_initial_board()

        run = True
        self.game.draw()
        pygame.display.update()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            
            pygame.event.clear()
            valid = True
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                #    can_t_go_left = self.game.board.can_t_go_left()
                #    can_t_go_right = self.game.board.can_t_go_right()
                #    can_t_go_up = self.game.board.can_t_go_up()
                #    can_t_go_down =self.game.board.can_t_go_down()

                #    print("can't go left: ", can_t_go_left)
                #    print("can't go right: ", can_t_go_right)
                #    print("can't go up: ", can_t_go_up)
                #    print("can't go down: ", can_t_go_down)

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_a]:
                        valid = self.game.move(0, False, False, False, False)
                        break
                    elif keys[pygame.K_s]:
                        valid =self.game.move(1, False, False, False, False)
                        break
                    elif keys[pygame.K_d]:
                        valid =self.game.move(2, False, False, False, False)
                        break
                    elif keys[pygame.K_w]:
                        valid =self.game.move(3, False, False, False, False)
            print("heuristic score: ", self.game.board.score)
            print("unchanged Score: ",self.game.board.unchangedScore)
            self.game.loop()
            self.game.draw()
            pygame.display.update()

            if not valid:
                run = False
                break

        pygame.quit()

    """
    This function will run the game on a specific NN
    """
    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.game.board.generate_initial_board()       
        self.game.draw()
        pygame.display.update()

        clock = pygame.time.Clock()
        run = True
        while run:
            print("loop in test_ai")
            clock.tick(4)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("quit in test_ai")
                    run = False
                    break


            flat_list = [item for sublist in self.game.board.get_log_list() for item in sublist]

            #equal to 1 If you can't go in that direction
            can_t_go_left = self.game.board.can_t_go_left()
            can_t_go_right = self.game.board.can_t_go_right()
            can_t_go_up = self.game.board.can_t_go_up()
            can_t_go_down =self.game.board.can_t_go_down()

            flat_list.append(can_t_go_left)
            flat_list.append(can_t_go_right)
            flat_list.append(can_t_go_up)
            flat_list.append(can_t_go_down)

            print(flat_list)

            output = net.activate(flat_list)

            print(output)
            decision = output.index(max(output))

            valid = self.game.move(decision, can_t_go_left, can_t_go_up, can_t_go_right, can_t_go_down)

            game_info = self.game.loop()
            self.game.draw()
            pygame.display.update()

            if not valid:
                self.calculate_fitness(genome, game_info)
                run = False
                break

        pygame.quit()


    """
    This function trains the AI: runs the NEAT evolutionary algorithm
    """
    def train_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
   #     self.game.draw()
   #     pygame.display.update()
        clock = pygame.time.Clock()
        while run:
            clock.tick(1500) #trying to slow it down
            pygame.event.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("quit in train_ai")
                    quit()

            flat_list = [item for sublist in self.game.board.get_log_list() for item in sublist]

            #equal to 1 If you can't go in that direction
            can_t_go_left = self.game.board.can_t_go_left()
            can_t_go_right = self.game.board.can_t_go_right()
            can_t_go_up = self.game.board.can_t_go_up()
            can_t_go_down =self.game.board.can_t_go_down()

            flat_list.append(can_t_go_left)
            flat_list.append(can_t_go_right)
            flat_list.append(can_t_go_up)
            flat_list.append(can_t_go_down)

            output = net.activate(flat_list)
            
            decision = output.index(max(output))

            valid = self.game.move(decision, can_t_go_left, can_t_go_up, can_t_go_right, can_t_go_down)

            game_info = self.game.loop()
       #     self.game.draw()
       #     pygame.display.update()

            if not valid:
                genome.fitness += self.game.board.score + self.game.board.unchangedScore
                run = False
                break

        return self.game.board.unchangedScore


######################## END OF NEATGame ##################################
"""
This function sets a score for each genome that will then be used to determine the better mutations
"""
def eval_genomes(genomes, config):
    width, height, header_size = 400, 400, 100
    window = pygame.display.set_mode((width, height + header_size))

    maxUnchangedScore = 0

    for i, (genome_id1, genome) in enumerate(genomes):
        genome.fitness = 0
        
        #since there is a probabilistic approach to this game, I want to reduce the luck factor
        for i in range(5):
            NEATgame = NEATGame([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], window, width, height, header_size)
        
            NEATgame.game.board.generate_initial_board()
            maxUnchangedScore = max(maxUnchangedScore, NEATgame.train_ai(genome, config))
    print("max unchanged Score: ", maxUnchangedScore)

"""
Run the evolutionary algorithm
Can be done from scratch or from a checkpoint (first line)
"""
def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1159')
    p = neat.Population(config)

    #the following modifications are used to finetune the learning process
    #we want a higher ratio of connections to nodes!!
    p.config.genome_config.node_add_prob = 0.05
    p.config.genome_config.node_delete_prob = 0.025

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(20)) #save a checkpoint every n generation

    numberOfGenerations = 10000
    winner = p.run(eval_genomes, numberOfGenerations)
    #winner is the first one to surpass the required fitness
    #or the best genome once the numberOfGenerations has been reached
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

"""
Test a specific genome
"""
def test_ai(config):
    width, height, header_size = 400, 400, 100
    window = pygame.display.set_mode((width, height + header_size))

    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = NEATGame([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], window, width, height, header_size)
    game.test_ai(winner, config)

"""
User can play the game
"""
def play_game():
    width, height, header_size = 400, 400, 100
    window = pygame.display.set_mode((width, height + header_size))

    game = NEATGame([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], window, width, height, header_size)
    game.play_game()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)
    #test_ai(config)
    #play_game()