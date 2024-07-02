import streamlit as st

def levenshtein_distance(source, target):
    matrix = []
    matrix.append([i for i in range(len(target)+1)])
    matrix.extend([[i] for i in range(1, len(source)+1)])

    for s in range(1, len(source)+1):
        for t in range(1, len(target)+1):
            del_cost = matrix[s-1][t] + 1
            ins_cost = matrix[s][t-1] + 1
            sub_cost = matrix[s-1][t-1] + (source[s-1] != target[t-1])
            matrix[s].append(min(del_cost, ins_cost, sub_cost))
    
    return matrix[-1][-1]

FILE_PATH = 'streamlit_project/data/vocab.txt'

def input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    dictionary = sorted(set([line.strip().lower() for line in lines]))
    return dictionary

words = input(FILE_PATH)

def main():
    st.title("Word Suggestion using Levenshtein Distance")
    input_word = st.text_input('Input:')

    if st.button("Suggest"):

        # Calculate levenshtein distance
        leven_dist = dict()
        for word in words:
            leven_dist[word] = levenshtein_distance(input_word, word)
        
        # Sorting distances from lowest to highest
        sorted_distances = dict(sorted(leven_dist.items(), key = lambda x: x[1]))
        suggested_word = list(sorted_distances.keys())[0]
        st.write('Suggested word: ', suggested_word)

        col1, col2 = st.columns(2)
        col1.write('Dictionary:')
        col1.write(words)
        
        col2.write('Distances:')
        col2.write(sorted_distances)

if __name__ == "__main__":
    main()