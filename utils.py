import database
import random

class game:
    def __init__(self, cid, level):
        self.cid = cid
        self.level = level
        self.completed = []
        self.letters = self.id_assignment()
        self.words = self.assing_word()
        self.word_progress = None
        self.dict_letter_selected = {}
        self.selected_letters = []
        self.dict_hint = {}
        
    
    def is_completed(self,word):
        if word in self.completed:
            return True
        return False
    
    def is_word_selected(self, word):
        if self.word_progress == word:
            return True
        return False

    def is_letter_selected(self, letter):
        if letter in self.selected_letters:
            return True
        return False

    def select_letter(self, letter_id):
        if self.word_progress != None:
            index = self.selected_letters.index(None)
            self.selected_letters[index] = letter_id

            # self.selected_letters.append(letter_id)
            print(self.word_progress.replace(' ','') , self.selected_letters)
            # if len(self.word_progress.replace(' ','')) == len(self.selected_letters):
            if None not in self.selected_letters:
                test_word = ''
                for i in self.selected_letters:
                    test_word += self.letters[i]

                for word in self.words:
                    print(word, test_word)
                    if word.replace(' ','') == test_word:
                        return word
                
                # if self.word_progress.replace(' ','') == test_word:
                #     return 'ok'
                else:
                    return 'no'
            else:
                return False

    def check_completed(self):
        if None not in self.selected_letters:
            test_word = ''
            for i in self.selected_letters:
                test_word += self.letters[i]
            if self.word_progress.replace(' ','') == test_word:
                return True
        else:
            return False

    def id_assignment(self):
        try:
            letters = database.select_one_letter(self.level)[0]
            id = 0
            dict_letters = {}
            for letter in letters['letter']:
                dict_letters[id] = letter
                id += 1
            return dict_letters
        except:
            return 'endgame'

        
    def assing_word(self):
        words = database.select_words(self.level)
        list_word = []
        for word in words:
            list_word.append(word['word'])
        return list_word

    def select_word_progress(self, word):
        self.word_progress = word
        list_none = []
        for i in word.replace(' ',''):
            list_none.append(None)

        if self.word_progress in self.dict_hint:
            if len(self.dict_hint[self.word_progress]) > 0:
                for key, val in self.dict_hint[self.word_progress].items():
                    list_none[key]= self.get_number_harf(val)
        self.selected_letters = list_none

    def insert_completed(self, word):
        self.completed.append(word)
        self.word_progress = None
        self.selected_letters = []
        if len(self.completed) == len(self.words):
            return 'ended'


    def wrong_completed(self):
        self.word_progress = self.word_progress
        list_none = []
        for i in self.word_progress.replace(' ',''):
            list_none.append(None)
        self.selected_letters = list_none

    def bazyabi(self):
        self.word_progress = self.word_progress
        list_none = []
        for i in self.word_progress.replace(' ',''):
            list_none.append(None)

        if self.word_progress in self.dict_hint:
            if len(self.dict_hint[self.word_progress]) > 0:
                for key, val in self.dict_hint[self.word_progress].items():
                    list_none[key]= self.get_number_harf(val)
        self.selected_letters = list_none

    def hint(self):
        self.dict_hint.setdefault(self.word_progress,{})
        list_harf = self.word_progress
        # if self.dict_hint[self.word_progress]

        non_empty_indices = [i for i, item in enumerate(list_harf) if item.strip()]

        while True:
            selected_index = random.choice(non_empty_indices)
            if self.selected_letters[selected_index] == None:
                break

        # پرینت ایندکس و مقدار انتخاب شده
        self.dict_hint.setdefault(self.word_progress,{})
        self.dict_hint[self.word_progress][selected_index] = list_harf[selected_index]
        print(f"Index: {selected_index}, Selected Item: {list_harf[selected_index]}")
        print(self.letters)
        self.selected_letters[selected_index] = self.get_number_harf(list_harf[selected_index])
        

    def get_number_harf(self, harf):
        for key, val in self.letters.items():
            if val == harf and key not in self.selected_letters:
                return key


    def check_letter_in_hint(self, letter):
        if self.word_progress in self.dict_hint:
            if len(self.dict_hint[self.word_progress]) > 0:
                list_letter_hint = []
                for i in self.dict_hint[self.word_progress]:
                    list_letter_hint.append(self.dict_hint[self.word_progress][i])
                if letter in list_letter_hint:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False