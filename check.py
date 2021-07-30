import sys
from PyQt5.QtWidgets import QWidget , QPushButton , QApplication , QLineEdit , QLabel , QPlainTextEdit , QMessageBox , \
    QGridLayout , QListWidget
from PyQt5.QtGui import QIcon , QFont
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
import datetime


class Show_window( QWidget ):
    def __init__( self ):
        QWidget.__init__( self )

    def init_ui( self , some_text ):
        self.setWindowTitle( 'База отправленных сообщений' )
        self.setFixedSize( 900 , 900 )
        self.move( 900 , 100 )
        self.setStyleSheet( 'background-color: rgb(24, 48, 73);color: honeydew;' )
        self.setWindowIcon( QIcon( 'startup_rocket_spaceship_launch_business_icon_191142 (1).png' ) )
        self.text_for_lineedit = QLabel( self )
        self.text_for_lineedit.move( 5 , 10 )
        self.some_text = some_text
        print( self.some_text )
        self.text_for_lineedit.setText( self.some_text )
        self.text_for_lineedit.setStyleSheet(
            'background-color: rgb(255,255,255);color:black;margin-left:25px;font-size:25px;' )

    def set_name( self , some_text ):
        self.some_text = some_text
        print( self.some_text )


class Data_window( QWidget ):
    def __init__( self ):
        QWidget.__init__( self )
        self.init_ui()

    def init_ui( self ):
        # -----------------------
        self.conn = sqlite3.connect( 'orders.db' )
        self.cur = self.conn.cursor()
        self.setWindowTitle( 'База отправленных сообщений' )
        self.setFixedSize( 500 , 500 )
        self.move( 900 , 100 )
        self.setStyleSheet( 'background-color: rgb(24, 48, 73);color: honeydew;' )
        self.setWindowIcon( QIcon( 'startup_rocket_spaceship_launch_business_icon_191142 (1).png' ) )
        # -----------------------
        self.cur.execute( "SELECT to_email FROM sended_emails;" )
        self.emails_data = self.cur.fetchall()
        self.cur.execute( "SELECT message FROM sended_emails;" )
        self.messages_for_emails = self.cur.fetchall()
        self.cur.execute( "SELECT text_data_and_time FROM sended_emails;" )
        self.times = self.cur.fetchall()
        # -----------------------
        layout = QGridLayout()
        self.setLayout( layout )
        self.listwidget = QListWidget()
        count = 0
        for i in zip( self.emails_data , self.times ):
            for j in i:
                print( j[ 0 ] )
        check = ''
        for emails in zip( self.emails_data , self.times ):
            for items in emails:
                check += items[ 0 ] + ' '
            self.listwidget.insertItem( count , check )
            check = ''
            count += 1
        self.listwidget.clicked.connect( self.on_click_db )
        layout.addWidget( self.listwidget )
        self.text_base = [ ]
        for i in self.messages_for_emails:
            self.text_base.append( i[ 0 ] )
        print( self.text_base )

    def on_click_db( self ):
        item = self.listwidget.currentIndex()
        print( self.text_base[ item.row() ] )
        self.window_3 = Show_window()
        self.window_3.init_ui( self.text_base[ item.row() ] )
        self.window_3.show()


class App( QWidget ):
    def __init__( self ):
        super( QWidget , self ).__init__()
        self.app = QApplication( sys.argv )
        self.init_ui()

    def init_ui( self ):
        # -----------------------
        self.window_2 = Data_window()
        # -----------------------
        self.conn = sqlite3.connect( 'orders.db' )
        self.cur = self.conn.cursor()
        self.cur.execute( """CREATE TABLE IF NOT EXISTS sended_emails(
                   to_email TEXT,
                   message TEXT,
                   text_data_and_time TEXT);
                """ )
        self.conn.commit()
        # -----------------------
        self.setFixedSize( 400 , 800 )
        self.move( 500 , 100 )
        self.setStyleSheet( 'background-color: rgb(24, 48, 73);color: honeydew;' )
        # -----------------------
        self.text_for_lineedit = QLabel( self )
        self.text_for_lineedit.move( 5 , 10 )
        self.text_for_lineedit.setText( 'Введите Email : ' )
        self.text_for_lineedit.setStyleSheet( "" )
        self.text_for_lineedit.setFont( QFont( 'Bitter' , 10 ) )
        # -----------------------
        self.textbox = QLineEdit( self )
        self.textbox.move( 5 , 40 )
        self.textbox.resize( 390 , 40 )
        self.textbox.setStyleSheet( 'background-color: rgb(184, 205, 228);'
                                    'color: rgb(37, 16, 37);'
                                    'font-size: 22px;' )
        # -----------------------
        self.plain_text = QPlainTextEdit( self )
        self.plain_text.insertPlainText( 'Введите сюда своё сообщение (╯°□°）╯︵ ┻━┻' )
        self.plain_text.resize( 390 , 500 )
        self.plain_text.move( 5 , 100 )
        self.holder_for_text = [ ]
        self.plain_text.textChanged.connect(
            lambda: self.holder_for_text.append( self.plain_text.document().toPlainText() ) )
        self.plain_text.setStyleSheet( 'background-color: rgb(184, 205, 228);'
                                       'color: rgb(37, 16, 37);'
                                       'font-size: 22px;' )
        # -----------------------
        self.push_button_submit = QPushButton( "Отправить сообщение" , self )
        self.push_button_submit.resize( 390 , 55 )
        self.push_button_submit.move( 0 , 740 )
        self.push_button_submit.setStyleSheet( "background-color: rgb(155, 155, 155);"
                                               "color:black;"
                                               "text-align: center;"
                                               "border: 1px solid rgb(0, 0, 0);margin-left:5px;" )
        self.push_button_submit.clicked.connect( self.on_click_send )
        # -----------------------
        self.button_to_db = QPushButton( 'Перейти в базу данных' , self )
        self.button_to_db.resize( 390 , 55 )
        self.button_to_db.move( 0 , 640 )
        self.button_to_db.setStyleSheet( "background-color: rgb(155, 155, 155);"
                                         "color:black;"
                                         "text-align: center;"
                                         "border: 1px solid rgb(0, 0, 0); margin-left:5px;" )

        self.button_to_db.clicked.connect( self.change_to_db_window )
        # -----------------------
        self.setWindowTitle( 'Отправка сообщений' )
        self.setWindowIcon( QIcon( 'startup_rocket_spaceship_launch_business_icon_191142 (1).png' ) )
        self.show()

    def on_click_send( self ):
        print( "pustota" )
        if self.textbox.text() is None or self.holder_for_text[ -1 ] is None or self.textbox.text() == '':
            print( "Пустые поля" )
        else:
            self.push_button_submit.setStyleSheet( "background-color: rgb(255,255,255);"
                                                   "color:black;"
                                                   "text-align: center;"
                                                   "border: 1px solid rgb(0, 0, 0);" )
            # -----------------------
            addr_from = "testovicht12@gmail.com"
            addr_to = self.textbox.text()
            password = "testovicht12123"
            msg = MIMEMultipart()
            # -----------------------
            msg[ 'From' ] = addr_from
            msg[ 'To' ] = addr_to
            msg[ 'Subject' ] = 'Сообщение с приложения!'
            # -----------------------
            body = self.holder_for_text[ -1 ]
            msg.attach( MIMEText( body , 'plain' ) )
            server = smtplib.SMTP( 'smtp.gmail.com' , 587 )
            # -----------------------
            server.starttls()
            server.login( addr_from , password )
            server.send_message( msg )
            server.quit()
            # -----------------------
            message_for_user = QMessageBox( self )
            message_for_user.setWindowTitle( "Успешная отправка" )
            message_for_user.setText( "Сообщение успешно отправлено " )
            message_for_user.setIcon( QMessageBox.Information )

            message_for_user.setStandardButtons( QMessageBox.Cancel | QMessageBox.Ok )
            message_for_user.setDefaultButton( QMessageBox.Ok )

            message_for_user.setDetailedText(
                "Вы можете просмотерть все отправленные сообщнеия в дополнительной вкладке , в основном меню" )
            message_for_user.setInformativeText(
                "Сообщение было отправленно на почту : " + self.textbox.text() + '.Пожалуйста,перепроверьте почту.' )
            x = message_for_user.exec_()
            holder = (addr_to , body , datetime.datetime.now())
            # print( holder )
            self.cur.execute( "SELECT * FROM sended_emails;" )
            # print( self.cur.fetchall() )
            self.cur.execute( "INSERT INTO sended_emails VALUES (?,?,?);" , holder )
            self.conn.commit()

    def change_to_db_window( self ):
        print( "Сработала функция изменения окна" )

        self.window_2.show()


if __name__ == '__main__':
    ex = QApplication( sys.argv )
    app = App()
    sys.exit( ex.exec_() )
