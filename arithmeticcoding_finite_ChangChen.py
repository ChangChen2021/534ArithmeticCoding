class ArithmeticEncoding:

    def __init__(self, frequency_table):

        self.probability_table = self.get_probability_table(frequency_table)

    def get_probability_table(self, frequency_table):
        """
        Calculates the probability table out of the frequency table.

        frequency_table: A table of the term frequencies.

        Returns the probability table.
        """
        total_frequency = sum(list(frequency_table.values()))

        probability_table = {}
        for key, value in frequency_table.items():
            probability_table[key] = value/total_frequency

        return probability_table
        
    def encode(self, msg, probability_table, R):
        
        msg = list(msg)
        encoder = []
        # define precision as number of bits used to represent numbers
        precision = 8
        whole = 2**precision
        
        # define p
        p = list(probability_table.values())
        x = list(probability_table.keys())
        # define c
        c = []
        for j in range(1, len(p)+1):
            c_j = 0
            for i in range (j-1):
                c_j = c_j + p[i] * R  
            c.append(c_j)
        # define d
        d = []
        for j in range(len(p)):
            d_j = c[j] + p[j] * R
            d.append(d_j)

        # a
        a = 0.0
        # b
        b = whole
        s = 0

        for i in range(0, len(msg)):
            w = b - a
            x_i = x.index(msg[i])
            b = a + round(w * d[x_i] / R)
            a = a + round(w * c[x_i] / R)
            while b < whole/2 or a > whole/2 :
                if b < whole/2:
                    codeword = [0]
                    for i in range(s):
                        codeword.append(1)
                    encoder.extend(codeword)
                    s = 0
                    a = 2*a
                    b = 2*b
                elif a > whole/2:
                    codeword = [1]
                    for i in range(s):
                        codeword.append(0)
                    encoder.extend(codeword)
                    s = 0
                    a = 2 * (a - whole/2)
                    b = 2 * (b - whole/2)
            while a > whole/4 and b < 3 * whole/4:
                s = s + 1
                a = 2 * (a - whole/4)
                b = 2 * (b - whole/4)
        s = s + 1
        if a <= whole/4:
            codeword = [0]
            for i in range(s):
                codeword.append(1)
            encoder.extend(codeword)
        else:
            codeword = [1]
            for i in range(s):
                codeword.append(0)
            encoder.extend(codeword)
        
        return encoder
    
    def decode(self, encoded_msg, probability_table, R):
        # define precision as number of bits used to represent numbers
        precision = 8
        whole = 2**precision

        z = 0
        a = 0
        b = whole
        decoded_msg = []
        
        # define p
        p = list(probability_table.values())
        # define c
        c = []
        for j in range(1, len(p)+1):
            c_j = 0
            for i in range (j-1):
                c_j = c_j + p[i] * R  
            c.append(c_j)
        # define d
        d = []
        for j in range(len(p)):
            d_j = c[j] + p[j] * R
            d.append(d_j)
        i = 1
        
        while (i <= precision) and (i <= len(encoded_msg)):
            if encoded_msg[i-1] == 1 : 
                z = z + 2**(precision - i)
            i = i + 1

        while 1:
            for j in range(len(p)):
                w = b - a
                b_0 = a + round(w * d[j]/ R)
                a_0 = a + round(w * c[j]/ R)  
                if (z >= a_0) and (z < b_0):
                    decoded_msg.append(j)
                    a = a_0
                    b = b_0
                    if j==0 : 
                        return decoded_msg
            while (b < whole/2) or (a > whole/2):
                if b < whole/2: 
                    a = 2 * a
                    b = 2 * b
                    z = 2 * z
                elif a > whole/2:
                    a = 2 * (a - whole/2)
                    b = 2 * (b - whole/2)
                    z = 2 * (z - whole/2)
                if (i <= len(encoded_msg)) and (encoded_msg[i-1] == 1):
                    z = z + 1
                i = i + 1
            while (a > whole/4) and (b < 3 * whole/4):
                a = 2 * (a - whole/4)
                b = 2 * (b - whole/4)
                z = 2 * (z - whole/4)
                if (i <= len(encoded_msg)) and (encoded_msg[i-1] == 1):
                    z = z + 1
                i = i + 1

frequency_table = {"0": 2,
                   "1": 4,
                   "2": 4}
AE = ArithmeticEncoding(frequency_table=frequency_table)

original_msg = "210"  
encoded_msg = AE.encode(original_msg, AE.probability_table, 100)
print("encoded_msg:", encoded_msg)

decoded_msg = AE.decode(encoded_msg, AE.probability_table, 100)
msg = "".join(str(e) for e in decoded_msg)
print("decoded_msg:", msg)



            
