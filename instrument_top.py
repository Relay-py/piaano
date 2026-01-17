import numpy as np


class InstrumentTop():
    def __init__(self,piano_corners,num_white_keys):
        self.piano_corners = piano_corners
        self.num_keys = num_white_keys
    
    def get_all_keys(self):
        '''
        Docstring for get_all_keys

        :param
             num_keys: Please provide the number of white keys only it should be divisible by 7 
                        for conviniency 
        
        :returns 
            lines_top_point : the top point for each line beetween two keys 
            lines_bottom_point : the bottom point for each line beetween two keys
            black_keys_top_point :for each line beetween two keys the top two corners of the black key that
                                    is supposed to be there if no black key is there then the list contain a None
            black_keys_bottom_point : same as the previous one but for the bottom two points
            
             

        '''

        
        lines_bottom_point = [(self.piano_corners[0]-self.piano_corners[1])*i+self.piano_corners[0] for i in range(self.num_keys+1)]
        lines_top_point = [(self.piano_corners[2]-self.piano_corners[3])*i+self.piano_corners[2]  for i in range(self.num_keys+1)]
        lines_top_point_draw =[]
        black_keys_top_point =[]
        black_keys_bottom_point =[]

        for i in range(len(lines_top_point)):
            if i % 3 == 0 or i % 7 == 0:
                lines_top_point_draw.append(lines_top_point[i])
                black_keys_top_point.append(None)
                black_keys_bottom_point.append(None)
                black_keys_top_point.append(None)
                black_keys_bottom_point.append(None)

            else: 
                value = ((lines_top_point[i] - lines_bottom_point[i]) * 3 / 5) + lines_bottom_point[i]
                previous = ((lines_top_point[i-1] - lines_bottom_point[i-1]) * 3 / 5) + lines_bottom_point[i-1]
                next  = ((lines_top_point[i+1] - lines_bottom_point[i-1]) * 3 / 5) + lines_bottom_point[i+1]

                lines_top_point_draw.append(((lines_top_point[i] - lines_bottom_point[i]) * 3 / 5) + lines_bottom_point[i])

                first_top_corner = (lines_top_point[i]-lines_top_point[i-1])/4 + lines_top_point[i-1]
                second_top_corner = (lines_top_point[i+1]-lines_top_point[i])/4 + lines_top_point[i]
                first_bottom_corner = (value -previous)/4 + previous
                second_botton_corner = (next - value)/4 + value
                black_keys_top_point.append(first_top_corner)
                black_keys_bottom_point.append(first_bottom_corner)
                black_keys_top_point.append(second_top_corner)
                black_keys_bottom_point.append(second_botton_corner)

        return (lines_top_point ,lines_bottom_point,black_keys_top_point , black_keys_bottom_point)
    


    
   

