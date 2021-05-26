
def get_date(data1, data2):
    # formatowanie daty
    data = ''
    # jesli miesiace sa te same
    if str(data2)[5:7] == str(data1)[5:7]:
        # jesli PJ dluzsza niz 1 dzień
        if str(data1)[8:10] != str(data2)[8:10]:
            # dzien-
            data += str(data1)[8:10] + ' - '
    else:
        # dzien.miesiac-
        data += str(data1)[8:10] + '.' + str(data1)[5:7] + ' - '
    # dzien.miesiac.rok
    data += str(data2)[8:10] + '.' + str(data2)[5:7] + '.' + str(data2)[0:4] + ' r.'
    return data
