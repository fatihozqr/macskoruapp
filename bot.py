- name: Botu calistir
        env:
          FD_API_KEY: ${{ secrets.FD_API_KEY }}
          RAPID_API_KEY: ${{ secrets.RAPID_API_KEY }}
        run: python bot.py
