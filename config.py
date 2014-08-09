import os

def Create_Key_File():
    '''

    Create the Twitter Oauth file on first run

    '''
    keys_f = os.environ.get(
            'HOME',
            os.environ.get(
                'USERPROFILE',
                '')) + os.sep + '.twitter_oauth'

    keyFile = open(keys_f,"w")
    try :
        keys = '''ck=3765316f446d4c436f38734d61394e78436446463468514275\n
        cs=65775a364252343742573976326e4e6732474c7a397639416678516f68545665796e63676c7179776d5561506b77534e6c4c
        \ntk=\n
        ts='''
        keyFile.write(keys)

    finally:
        keyFile.close()
    
