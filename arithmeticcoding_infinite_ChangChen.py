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

    def encode(self, msg, probability_table):
        
        msg = list(msg)
        encoder = []

        # define p
        p = list(probability_table.values())
        x = list(probability_table.keys())
        # define c
        c = []
        for j in range(1, len(p)+1):
            c_j = 0
            for i in range (j-1):
                c_j = c_j + p[i]  
            c.append(c_j)
        # define d
        d = []
        for j in range(len(p)):
            d_j = c[j] + p[j]
            d.append(d_j)

        # a
        a = 0.0
        b = 1.0
        for i in range(0, len(msg)):
            w = b - a
            x_i = x.index(msg[i])
            b = a + w * d[x_i]
            a = a + w * c[x_i]
        # b
        s = 0
        while b < 0.5 or a > 0.5 :
            if b < 0.5:
                encoder.append(0)
                a = 2 * a 
                b = 2 * b
            elif a > 0.5:
                encoder.append(1)
                a = 2 * (a - 0.5)
                b = 2 * (b - 0.5)
        while a > 0.25 and b < 0.75:
            s = s + 1
            a = 2 * (a - 0.25)
            b = 2 * (b - 0.25)
        s = s + 1
        if a <= 0.25:
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
    
    def decode(self, encoded_msg, probability_table):
        def bin2dec(bin):
            dec = 0
            for i, x in enumerate(bin):
                dec += 2**(-i-1)*x
            return dec

        z = bin2dec(encoded_msg)
        a = 0
        b = 1
        # define p
        p = list(probability_table.values())
        x = list(probability_table.keys())
        # define c
        c = []
        for j in range(1, len(p)+1):
            c_j = 0
            for i in range (j-1):
                c_j = c_j + p[i]  
            c.append(c_j)
        # define d
        d = []
        for j in range(len(p)):
            d_j = c[j] + p[j]
            d.append(d_j)
        
        decoded_msg = []
        while 1:
            for j in range(len(p)):
                w = b - a
                b_0 = a + w * d[j]
                a_0 = a + w * c[j]
                if (z >= a_0) and (z < b_0):
                    decoded_msg.append(x[j])
                    a = a_0
                    b = b_0
                    if j==0 : 
                        return decoded_msg

frequency_table = {"0": 2,
                   "1": 4,
                   "2": 4}
AE = ArithmeticEncoding(frequency_table=frequency_table)

original_msg = "210"  
encoded_msg = AE.encode(original_msg, AE.probability_table)
print("encoded_msg:", encoded_msg)
decoded_msg = AE.decode(encoded_msg, AE.probability_table)
msg = "".join(str(e) for e in decoded_msg)
print("decoded_msg:", msg)



            
