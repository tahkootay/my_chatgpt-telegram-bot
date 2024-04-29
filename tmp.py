user_choice_model = {'gpt-4-turbo','gpt-4-1106','gpt-3.5-turbo'}
command_text = '/settings system все ответы начинай'
# Разделяем команду и аргументы
parts = command_text.split(maxsplit=2) #
print(parts)   
if len(parts) == 3:
        if parts[1]=='model' and parts[2] in user_choice_model:
           print('да')
elif len(parts) == 2:
      if parts[1]=='model':
          print('model')  

