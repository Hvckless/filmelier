import numpy as np

class Main:

    def __init__(self):
        pass

    def helloworld(self):
        print("HELLO WORLD!")

        helloworld:list[float] = [0.1,0.2,0.3]
        mp_array:list[float] = [1,10,100]

        np_helloworld = np.array(helloworld)
        mp_np_array:np.ndarray = np.array(mp_array)

        

        total_array:list[np.ndarray] = []

        for i in range(5):
            _array:np.ndarray = np_helloworld.copy()

            for j in range(i):
                _array = _array * mp_np_array


            total_array.append(_array)

        final_np_array = np.array(total_array)
        print(final_np_array)
        print(final_np_array * mp_np_array)


        hellokinggod = [
            [1,2,3],
            [1,2,3],
            [1,2,3]
        ]

        hellokinggod_mp = [
            2,2,2
        ]

        print(np.array(hellokinggod) * np.array(hellokinggod_mp))
        

        



if __name__ == "__main__":
    app = Main()

    app.helloworld()