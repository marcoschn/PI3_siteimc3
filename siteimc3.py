from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb

from data import data_loader

import MySQLdb.cursors
import re
import datetime





app=Flask(__name__)


app.secret_key = 'passpi2univesp'

app.config['MYSQL_HOST'] = '212.85.12.121'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'UnivPi2025!'
app.config['MYSQL_DB'] = 'univespi3'

mysql = MySQL(app)


@app.route("/")
def index():
    session['loggedin'] = False
    return render_template("index.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
    session['loggedin'] = False
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        username = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE email = % s AND senha = % s', (username, password, ))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['codusuario']
            session['username'] = account['nome']
            session['email'] = account['email']
            msg = 'Logado com sucesso!'
            return redirect(url_for('home'))
        else:
            msg = 'Email ou senha incorretos'
    return render_template('login.html', msg = msg)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if session['loggedin'] == True:
        bemvindo = 'Bem-vindo(a), ' + session['username'] + '! - (seu número id é: ' + str(session['id']) + ')'
        cursorregistros = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
                        select 
        	                registros.codregistro as id, 
        	                date_format(registros.dtregistro,'%%d/%%m/%%Y') as dataregistro, 
        	                registros.alturam, 
        	                registros.pesokg, 
        	                format(((pesokg) / ((alturam)*(alturam))),1) as imc, 
        	                (case
        		                when (pesokg)/((alturam)*(alturam)) < 18.5 then 'baixo peso' 
        		                when (pesokg)/((alturam)*(alturam)) >=18.5 and (pesokg)/((alturam)*(alturam)) < 25 then 'normal' 
        		                when (pesokg)/((alturam)*(alturam)) >=25 and (pesokg)/((alturam)*(alturam)) < 30 then 'sobrepeso' 
        		                when (pesokg)/((alturam)*(alturam)) >=30 and (pesokg)/((alturam)*(alturam)) < 35 then 'obesidade classe I' 
        		                when (pesokg)/((alturam)*(alturam)) >=35 and (pesokg)/((alturam)*(alturam)) < 40 then 'obesidade classe II' 
        		                when (pesokg)/((alturam)*(alturam)) >=40 then 'obesidade classe III' 
        		                else '0'
        	                end) as status
                        from 
        	                univespi3.registros 
                        inner join univespi3.usuarios on registros.regcodusuario = usuarios.codusuario
                        where 
        	                registros.regcodusuario = % s 
                        order by 
        	            dtregistro desc
                    """
        cursorregistros.execute(sql, (session['id'],))
        resultados = cursorregistros.fetchall()
        # for rows in resultados:
        #    print(rows)
        return render_template('home.html', bemvindo=bemvindo, resultados=resultados)
    return redirect(url_for('login'))


@app.route('/visualizarcomp', methods=['GET', 'POST'])
def visualizarcomp():
    if session['loggedin'] == True:
        cdestinatarios = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sqldestinatarios = """SELECT 
        	        usuorigem.nome AS usuorigemnome, 
        	        dadosusuorigem.nome AS nomecompletoorigem, 
        	        univespi3.compartilhamento.autorizar, 
        	        univespi3.compartilhamento.usuorigem, 
        	        univespi3.compartilhamento.usudestino,
        	        dadosusuorigem.dtnascimento,
	                dadosusuorigem.sexo  
                FROM 
        	        univespi3.usuarios usuorigem 
        	        INNER JOIN univespi3.dadosusuario dadosusuorigem 
        	        ON usuorigem.codusuario = dadosusuorigem.codusuario 
        	        INNER JOIN univespi3.compartilhamento 
        	        ON usuorigem.codusuario = univespi3.compartilhamento.usuorigem 
        	        INNER JOIN univespi3.usuarios usudestino 
        	        ON univespi3.compartilhamento.usudestino = usudestino.codusuario 
        	        INNER JOIN univespi3.dadosusuario dadosusuodestino 
        	        ON usudestino.codusuario = dadosusuodestino.codusuario 
                WHERE 
        	        univespi3.compartilhamento.usudestino = % s
        	    order by 
        	        usuorigemnome"""
        cdestinatarios.execute(sqldestinatarios, (session['id'],))
        vdestinatarios = cdestinatarios.fetchall()
        rcdestinatario=cdestinatarios.rowcount
        print("registro")
        print(vdestinatarios)
        pesokg=0
        dadosgraf=0
        dtregistro=0
        iniciargrafico=0

        if rcdestinatario!=0:
            #return render_template('visualizarcomp.html', vdestinatarios=vdestinatarios, template_labels=dtregistro,
            #                   template_values_confirmed=pesokg, dadosgraf=dadosgraf)
            return render_template('visualizarcomp.html', vdestinatarios=vdestinatarios, iniciargrafico=iniciargrafico)
        else:
            vdestinatarios=0
            #return render_template('visualizarcomp.html', vdestinatarios=vdestinatarios, template_labels=dtregistro,
            #                   template_values_confirmed=pesokg, dadosgraf=dadosgraf)
            return render_template('visualizarcomp.html', vdestinatarios=vdestinatarios, iniciargrafico=iniciargrafico)

    return redirect(url_for('login'))


@app.route('/ver_comp', methods=['GET', 'POST'])
def ver_comp():
    if session['loggedin'] == True:

        if request.method == 'POST':
            idorigem = request.form['destinatario']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sqlorigem = """
                            select 
            	                registros.codregistro as id, 
            	                date_format(registros.dtregistro,'%%d/%%m/%%Y') as dataregistro, 
            	                registros.alturam, 
            	                registros.pesokg, 
            	                format(((pesokg) / ((alturam)*(alturam))),1) as imc, 
            	                (case
            		                when (pesokg)/((alturam)*(alturam)) < 18.5 then 'baixo peso' 
            		                when (pesokg)/((alturam)*(alturam)) >=18.5 and (pesokg)/((alturam)*(alturam)) < 25 then 'normal' 
            		                when (pesokg)/((alturam)*(alturam)) >=25 and (pesokg)/((alturam)*(alturam)) < 30 then 'sobrepeso' 
            		                when (pesokg)/((alturam)*(alturam)) >=30 and (pesokg)/((alturam)*(alturam)) < 35 then 'obesidade classe I' 
            		                when (pesokg)/((alturam)*(alturam)) >=35 and (pesokg)/((alturam)*(alturam)) < 40 then 'obesidade classe II' 
            		                when (pesokg)/((alturam)*(alturam)) >=40 then 'obesidade classe III' 
            		                else '0'
            	                end) as status
                            from 
            	                univespi3.registros 
                            inner join univespi3.usuarios on registros.regcodusuario = usuarios.codusuario
                            where 
            	                registros.regcodusuario = % s order by dtregistro asc"""
            print(idorigem)
            print(sqlorigem)
            cursor.execute(sqlorigem, (idorigem,))
            linhas=cursor.execute(sqlorigem, (idorigem,))
            dadoscomp = cursor.fetchall()

            print("linhas")
            print(linhas)
            print("dadoscomp")
            print(dadoscomp)

            #preparar grafico
            #dadosgraf = cursor.fetchall()

            graphdtregistro = []
            graphpesokg = []
            for row in dadoscomp:
                graphdtregistro.append(row['dataregistro'])
                graphpesokg.append(row['pesokg'])
            #fim

            print("dadosgraf")
            print(graphpesokg)
            print(graphdtregistro)

            sqldadosusuario="""
                                SELECT 
	                            univespi3.usuarios.codusuario as codusuario,
	                            univespi3.usuarios.email,
	                            univespi3.usuarios.nome,
	                            univespi3.dadosusuario.nome as ncompleto,
	                            univespi3.dadosusuario.dtnascimento,
	                            univespi3.dadosusuario.sexo
                                FROM 
	                                univespi3.usuarios 
	                            INNER JOIN univespi3.dadosusuario ON univespi3.usuarios.codusuario = univespi3.dadosusuario.codusuario 
                                WHERE 
	                                univespi3.usuarios.codusuario = % s"""
            cursor.execute(sqldadosusuario, (idorigem,))
            dadosusuario=cursor.fetchone()

            print("dadosusuario")
            print(dadosusuario)
            ncompleto=dadosusuario['ncompleto']
            idusuario=dadosusuario['codusuario']

            cdestinatarios = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sqldestinatarios = """SELECT 
                        	        usuorigem.nome AS usuorigemnome, 
                        	        dadosusuorigem.nome AS nomecompletoorigem, 
                        	        univespi3.compartilhamento.autorizar, 
                        	        univespi3.compartilhamento.usuorigem, 
                        	        univespi3.compartilhamento.usudestino,
                        	        dadosusuorigem.dtnascimento,
	                                dadosusuorigem.sexo 
                                FROM 
                        	        univespi3.usuarios usuorigem 
                        	        INNER JOIN univespi3.dadosusuario dadosusuorigem 
                        	        ON usuorigem.codusuario = dadosusuorigem.codusuario 
                        	        INNER JOIN univespi3.compartilhamento 
                        	        ON usuorigem.codusuario = univespi3.compartilhamento.usuorigem 
                        	        INNER JOIN univespi3.usuarios usudestino 
                        	        ON univespi3.compartilhamento.usudestino = usudestino.codusuario 
                        	        INNER JOIN univespi3.dadosusuario dadosusuodestino 
                        	        ON usudestino.codusuario = dadosusuodestino.codusuario 
                                WHERE 
                        	        univespi3.compartilhamento.usudestino = % s
                        	    order by 
                        	        usuorigemnome"""
            cdestinatarios.execute(sqldestinatarios, (session['id'],))
            vdestinatarios = cdestinatarios.fetchall()
            rcdestinatario = cdestinatarios.rowcount

            print(vdestinatarios)
            if rcdestinatario != 0:
                #calculo da tmb (taxa metabólica basal)
                i=0
                for data in dadoscomp:
                    if i==0:
                        if linhas > 0:
                            dtprimeiroregistro = data['dataregistro']
                            pesoinicial = data['pesokg']

                    else:
                        if i == (linhas - 1):
                            alturacm = data['alturam'] * 100
                            dataregistro = data['dataregistro']
                            peso = data['pesokg']
                    i=i+1

                if linhas > 0:

                    anodtregistro = dataregistro[-4:]
                    mesdtregistro = dataregistro[3:5]
                    diadtregistro=dataregistro[0:2]
                    anoprimeiroregistro = dtprimeiroregistro[-4:]
                    mesprimeiroregistro = dtprimeiroregistro[3:5]
                    diaprimeiroregistro = dtprimeiroregistro[0:2]

                    d1=datetime.date(int(anodtregistro),int(mesdtregistro),int(diadtregistro))
                    dprimeiroreg=datetime.date(int(anoprimeiroregistro),int(mesprimeiroregistro),int(diaprimeiroregistro))

                    datediff=(d1 - dadosusuario['dtnascimento'])
                    idade=round(datediff.days / 365,2)

                    datediffperiodo=(d1 - dprimeiroreg)
                    periodomedicao=round(datediffperiodo.days / 30.5,2)
                    difpeso=peso - pesoinicial
                    iniciargrafico=1


                    #cálculo Fórmula de Harris-Benedict (versão revisada) da taxa metabólica basal

                    if dadosusuario['sexo']=='M':
                        tmb=round(88.362 + (13.397 * peso) + (4.799 * alturacm) - (5.677 * idade), 0)
                        tmbsedentario = round(1.2 * tmb,0)
                        tmbpoucoativo = round(1.375 * tmb,0)
                        tmbativo = round(1.55 * tmb,0)
                        tmbmuitoativo = round(1.725 * tmb,0)
                        tmbextremamenteativo = round(1.9 * tmb,0)

                    else:
                        tmb=round(447.593 + (9.247 * peso) + (3.098 * alturacm) - (4.330 * idade), 0)
                        tmbsedentario = round(1.2 * tmb,0)
                        tmbpoucoativo = round(1.375 * tmb,0)
                        tmbativo = round(1.55 * tmb,0)
                        tmbmuitoativo = round(1.725 * tmb,0)
                        tmbextremamenteativo = round(1.9 * tmb,)

                    print(tmb)

                    return render_template('visualizarcomp.html', vdestinatarios=vdestinatarios, dadoscomp=dadoscomp, dadosusuario=dadosusuario, tmb=tmb, dataregistro=dataregistro, tmbsedentario=tmbsedentario, tmbpoucoativo=tmbpoucoativo, tmbativo=tmbativo, tmbmuitoativo=tmbmuitoativo, tmbextremamenteativo=tmbextremamenteativo, ncompleto=ncompleto, idusuario=idusuario, periodomedicao=periodomedicao, difpeso=difpeso, graphdtregistro=graphdtregistro, graphpesokg=graphpesokg, iniciargrafico=iniciargrafico)

                else:
                    return render_template('visualizarcomp.html', vdestinatarios=vdestinatarios, dadoscomp=dadoscomp, dadosusuario=dadosusuario)

            else:
                vdestinatarios = 0
                return render_template('visualizarcomp.html', vdestinatarios=vdestinatarios, dadoscomp=dadoscomp, dadosusuario=dadosusuario)

    else:
        return redirect(url_for('index'))



@app.route('/perfil', methods =['GET', 'POST'])
def perfil():
    if session['loggedin'] == True:
            sqlusuario="""SELECT 
            dadosusuario.nome as nomecompleto, 
            DATE_FORMAT(dadosusuario.dtnascimento, '%Y-%m-%d') as dtnasc, 
            usuarios.codusuario as idusuario, 
            usuarios.nome as nome, 
            usuarios.email as email  ,
            dadosusuario.sexo as sexo ,
            usuarios.senha as senha
            FROM univespi3.usuarios 
            inner JOIN univespi3.dadosusuario  
            ON usuarios.codusuario = dadosusuario.codusuario 
            WHERE usuarios.codusuario = """ + str(session['id'])
            print(sqlusuario)

            cursorperfil = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursorperfil.execute(sqlusuario)
            perfilusuario = cursorperfil.fetchall()
            print(perfilusuario)
            return render_template('perfil.html', perfilusuario=perfilusuario[0])
    else:
        return redirect(url_for('index'))

@app.route('/atualizaperfil', methods =['GET', 'POST'])
def atualizaperfil():
    if session['loggedin'] == True:
        if request.method == 'POST':
            usuario= request.form['nomeusuario']
            usuarioinicial=request.form['usuarioinicial']
            emailinicial=request.form['emailinicial']
            email = request.form['emailusuario']
            nomecompleto = request.form['nomecompleto']
            dtnascimento = request.form['dtnasc']
            sexo = request.form['sexo']
            senha=request.form['senha']
            senharepita = request.form['senharepita']
            if usuario != usuarioinicial:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM usuarios WHERE nome = % s', (usuario,))
                account = cursor.fetchone()
                if account:
                    problemausuario = 1
                else:
                    problemausuario = 0
            else:
                problemausuario = 0

            if email != emailinicial:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT * FROM usuarios WHERE nome = % s', (usuario,))
                emailusu = cursor.fetchone()
                if emailusu:
                    problemaemail = 1
                else:
                    problemaemail = 0
            else:
                problemaemail = 0

            if senha != senharepita:
                problemasenha= 1
            else:
                problemasenha= 0

            resultado = problemausuario + problemaemail + problemasenha
            print("resultado:" + str(resultado))
            print(usuario)
            print(usuarioinicial)
            print(nomecompleto)
            print(dtnascimento)
            print(email)
            print(emailinicial)
            print(senha)
            print(senharepita)
            print(sexo)

            if resultado == 0:
                cursorregistros = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                sqlatualizaperfil="UPDATE dadosusuario SET nome = '" + nomecompleto + "', dtnascimento='" + dtnascimento + "', sexo='" + sexo + "' where codusuario=" + str(session['id'])
                cursorregistros.execute(sqlatualizaperfil)
                sqlatualizausuario = "UPDATE usuarios SET nome = '" + usuario + "', email='" + email + "', senha='" + senha + "' where codusuario=" + str(session['id'])
                cursorregistros.execute(sqlatualizausuario)
                mysql.connection.commit()
                flash('Perfil atualizado.')
                return redirect(url_for('home'))
            else:
                if problemausuario==1:
                    flash('Esse usuario já existe. Digite outro nome de usuário')
                if problemasenha==1:
                    flash('As senhas não são iguais. Por favor, confirme corretamente sua senha.')
                if problemaemail==1:
                    flash('Esse email já está sendo utilizado por alguém. Por favor, escolha outro.')
                #return redirect(url_for('home'))
                return redirect(request.referrer)

    else:
        return redirect(url_for('index'))

@app.route('/grafico', methods=['GET', 'POST'])
def grafico():
    """
    the main route rendering index.html
    :return:
    """
    if session['loggedin'] == True:
        cursordadosgraf = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = """
                                select 
                	                registros.codregistro as id, 
                	                date_format(registros.dtregistro,'%%d/%%m/%%Y') as dataregistro, 
                	                registros.alturam, 
                	                registros.pesokg, 
                	                format(((pesokg) / ((alturam)*(alturam))),1) as imc, 
                	                (case
                		                when (pesokg)/((alturam)*(alturam)) < 18.5 then 'baixo peso' 
                		                when (pesokg)/((alturam)*(alturam)) >=18.5 and (pesokg)/((alturam)*(alturam)) < 25 then 'normal' 
                		                when (pesokg)/((alturam)*(alturam)) >=25 and (pesokg)/((alturam)*(alturam)) < 30 then 'sobrepeso' 
                		                when (pesokg)/((alturam)*(alturam)) >=30 and (pesokg)/((alturam)*(alturam)) < 35 then 'obesidade classe I' 
                		                when (pesokg)/((alturam)*(alturam)) >=35 and (pesokg)/((alturam)*(alturam)) < 40 then 'obesidade classe II' 
                		                when (pesokg)/((alturam)*(alturam)) >=40 then 'obesidade classe III' 
                		                else '0'
                	                end) as status
                                from 
                	                univespi3.registros 
                                inner join univespi3.usuarios on registros.regcodusuario = usuarios.codusuario
                                where 
                	                registros.regcodusuario = % s 
                                order by 
                	            dtregistro asc
                            """
        cursordadosgraf.execute(sql, (session['id'],))
        dadosgraf = cursordadosgraf.fetchall()

        dtregistro=[]
        pesokg=[]
        for row in dadosgraf:
            dtregistro.append(row['dataregistro'])
            pesokg.append(row['pesokg'])

        return render_template('grafico.html', template_labels=dtregistro,
                               template_values_confirmed=pesokg, dadosgraf=dadosgraf)

    else:
        return redirect(url_for('index'))


@app.route('/compartilhamento', methods=['GET', 'POST'])
def compartilhamento():
    if session['loggedin'] == True:
        cursorcompartilhamento = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sqlcompartilhamento="""SELECT 
	        usudestino.nome AS usudestinonome, 
	        dadosusuodestino.nome AS nomecompletodestino, 
	        univespi3.compartilhamento.autorizar, 
	        univespi3.compartilhamento.usuorigem, 
	        univespi3.compartilhamento.usudestino 
        FROM 
	        univespi3.usuarios usuorigem 
	        INNER JOIN univespi3.dadosusuario dadosusuorigem 
	        ON usuorigem.codusuario = dadosusuorigem.codusuario 
	        INNER JOIN univespi3.compartilhamento 
	        ON usuorigem.codusuario = univespi3.compartilhamento.usuorigem 
	        INNER JOIN univespi3.usuarios usudestino 
	        ON univespi3.compartilhamento.usudestino = usudestino.codusuario 
	        INNER JOIN univespi3.dadosusuario dadosusuodestino 
	        ON usudestino.codusuario = dadosusuodestino.codusuario 
        WHERE 
	        univespi3.compartilhamento.usuorigem = % s
	    order by 
	        usudestino"""

        cursorcompartilhamento.execute(sqlcompartilhamento, (session['id'],))
        dadoscompartilhamento = cursorcompartilhamento.fetchall()

        return render_template('compartilhamento.html', dadoscompartilhamento=dadoscompartilhamento)

    else:
        return redirect(url_for('index'))

@app.route('/add_compartilhamento', methods=['GET', 'POST'])
def add_compartilhamento():
    if session['loggedin'] == True:

        if request.method == 'POST':
            idcompartilhar = request.form['idcompartilhar']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sqlcompartilhar='insert into compartilhamento values (' +  str(session['id']) + ', ' + idcompartilhar + ', true)'
            print(sqlcompartilhar)
            cursor.execute(sqlcompartilhar)
            mysql.connection.commit()
            flash('Compartilhado com sucesso')

            return redirect(url_for('compartilhamento'))

    else:
        return redirect(url_for('index'))

@app.route('/delcompartilhamento/<string:id>', methods=['POST', 'GET'])
def delcompartilhamento(id):
    if session['loggedin'] == True:
        querysql = "delete from compartilhamento where usudestino=" + id + " and usuorigem=" + str(session['id'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(querysql)
        mysql.connection.commit()
        flash('Compartilhamento removido.')

        return redirect(url_for('compartilhamento'))

    else:
        return redirect(url_for('index'))


@app.route('/sugestoes', methods=['GET', 'POST'])
def sugestoes():
    if session['loggedin'] == True:
        cursorsugestoes = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sqldestinatarios = """SELECT 
        	        usuorigem.nome AS usuorigemnome, 
        	        dadosusuorigem.nome AS nomecompletoorigem, 
        	        univespi3.compartilhamento.autorizar, 
        	        univespi3.compartilhamento.usuorigem, 
        	        univespi3.compartilhamento.usudestino 
                FROM 
        	        univespi3.usuarios usuorigem 
        	        INNER JOIN univespi3.dadosusuario dadosusuorigem 
        	        ON usuorigem.codusuario = dadosusuorigem.codusuario 
        	        INNER JOIN univespi3.compartilhamento 
        	        ON usuorigem.codusuario = univespi3.compartilhamento.usuorigem 
        	        INNER JOIN univespi3.usuarios usudestino 
        	        ON univespi3.compartilhamento.usudestino = usudestino.codusuario 
        	        INNER JOIN univespi3.dadosusuario dadosusuodestino 
        	        ON usudestino.codusuario = dadosusuodestino.codusuario 
                WHERE 
        	        univespi3.compartilhamento.usudestino = % s
        	    order by 
        	        usuorigemnome"""

        cursorsugestoes.execute(sqldestinatarios, (session['id'],))
        dadosdestinatarios = cursorsugestoes.fetchall()
        rc=cursorsugestoes.rowcount

        cursormsgsugestoes = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sqlmsgsugestoes="""SELECT 
                univespi3.sugestoes.idmsg as idmsg,
	            univespi3.dadosusuario.nome as nomeorigem, 
	            univespi3.sugestoes.de as idorigem, 
	            sugestoes.dt as dtmsg, 
	            univespi3.sugestoes.mensagem as msg 
            FROM 
	            univespi3.usuarios 
	            INNER JOIN univespi3.sugestoes 
	            ON univespi3.usuarios.codusuario = univespi3.sugestoes.de 
	            INNER JOIN univespi3.dadosusuario 
	            ON univespi3.usuarios.codusuario = univespi3.dadosusuario.codusuario 
            WHERE 
	            univespi3.sugestoes.para = %s order by dtmsg desc"""
        cursormsgsugestoes.execute(sqlmsgsugestoes, (session['id'],))
        dadosmsgsugestoes = cursormsgsugestoes.fetchall()
        rcmsgsugestoes = cursormsgsugestoes.rowcount

        if rc !=0:
            if rcmsgsugestoes!=0:
                return render_template('sugestoes.html', dadosdestinatarios=dadosdestinatarios, dadosmsgsugestoes=dadosmsgsugestoes)
            else:
                dadosmsgsugestoes=0
                return render_template('sugestoes.html', dadosdestinatarios=dadosdestinatarios,
                                       dadosmsgsugestoes=dadosmsgsugestoes)
        else:
            if rcmsgsugestoes != 0:
                dadosdestinatarios=0
                return render_template('sugestoes.html', dadosdestinatarios=dadosdestinatarios,dadosmsgsugestoes=dadosmsgsugestoes)
            else:
                dadosmsgsugestoes = 0
                dadosdestinatarios = 0
                return render_template('sugestoes.html', dadosdestinatarios=dadosdestinatarios,
                                       dadosmsgsugestoes=dadosmsgsugestoes)
    else:
        return redirect(url_for('index'))



@app.route('/add_sugestao', methods=['GET', 'POST'])
def add_sugestao():
    if session['loggedin'] == True:

        if request.method == 'POST':
            iddestinatario = request.form['destinatario']
            textosugestao=request.form['sugestaomsg']
            #dtsugestao=datetime.datetime.now()
            now = datetime.datetime.now()
            dtsugestao = now.strftime("%Y-%m-%d %H:%M:%S")
            print(iddestinatario)
            #print(textosugestao)
            print(dtsugestao)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            sqlsugestao="insert into sugestoes values (NULL, " +  str(session['id']) + ", " + str(iddestinatario) + ", '" + str(dtsugestao) + "', '" + textosugestao + "')"
            print(sqlsugestao)
            cursor.execute(sqlsugestao)
            mysql.connection.commit()
            flash('Sugestao enviada com sucesso')

            return redirect(url_for('sugestoes'))

    else:
        return redirect(url_for('index'))


@app.route('/delsugestao/<string:id>', methods=['GET', 'POST'])
def delsugestao(id):
    if session['loggedin'] == True:
        querysql = "delete from sugestoes where idmsg=" + id
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(querysql)
        mysql.connection.commit()
        flash('Sugestão removida.')

        return redirect(url_for('sugestoes'))

    else:
        return redirect(url_for('index'))


@app.route('/add_registro', methods=['GET', 'POST'])
def add_registro():
    if session['loggedin'] == True:
        #conn = mysql.connect()
        #cur = conn.cursor(pymysql.cursors.DictCursor)
        if request.method == 'POST':
            dtregistro = request.form['dtregistro']
            alturam = request.form['alturam']
            pesokg = request.form['pesokg']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO registros VALUES (NULL, % s, % s, % s, % s)',
                           (pesokg, alturam, dtregistro, session['id'],))
            mysql.connection.commit()
            flash('Medição adicionada com sucesso')

            return redirect(url_for('home'))

    else:
        return redirect(url_for('index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_medicao(id):
    #print(id)
    if session['loggedin'] == True:
        querysql="select codregistro, DATE_FORMAT(dtregistro, '%Y-%m-%d') as dt, alturam, pesokg from univespi3.registros where codregistro=" + id
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(querysql)
        data = cursor.fetchall()

        cursor.close()

        return render_template('edit.html', registro=data[0])
    else:
        return redirect(url_for('index'))

@app.route('/update/<id>', methods=['POST'])
def update_medicao(id):
    if session['loggedin'] == True:
        if request.method == 'POST':
            dtregistro = request.form['dtregistro']
            pesokg = request.form['pesokg']
            alturam = request.form['alturam']

            bemvindo = 'Bem-vindo(a), ' + session['username'] + '!'
            cursorregistros = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursorregistros.execute("""
                UPDATE registros
                SET dtregistro = %s,
                    pesokg = %s,
                    alturam = %s
                WHERE codregistro = %s
            """, (dtregistro, pesokg, alturam, id))
            mysql.connection.commit()
            flash('Registro atualizado.')

            return redirect(url_for('home'))
    else:
        return redirect(url_for('index'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_employee(id):
    if session['loggedin'] == True:
        querysql = "delete from registros where codregistro=" + id
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(querysql)
        mysql.connection.commit()
        flash('Medição removida.')

        return redirect(url_for('home'))

    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/registrar', methods =['GET', 'POST'])
def registrar():
    msg = ''
    if request.method == 'POST' and 'nome' in request.form and 'password' in request.form and 'passwordconf' in request.form and 'email' in request.form and 'dtnasc' in request.form and 'sexo' in request.form:
        username = request.form['nome']
        password = request.form['password']
        passwordconf = request.form['passwordconf']
        email = request.form['email']
        dtnasc = request.form['dtnasc']
        sexo = request.form['sexo']

        print(sexo)
        print(dtnasc)


        if password == passwordconf :
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM usuarios WHERE email = % s', (email, ))
            account = cursor.fetchone()
            if account:
                msg = 'Esse email já está cadastrado. Use outro'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Email inválido'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Nome deve conter apenas letras e números !'
            elif not username or not password or not email:
                msg = 'Por favor, preencha seus dados!'
            else:
                cursor.execute('INSERT INTO usuarios VALUES (NULL, % s, % s, % s)', (email, password, username, ))
                cursor.execute('select last_insert_id() from usuarios')
                idusuario=cursor.lastrowid
                #print(idusuario)
                sqlinsertdados="INSERT INTO dadosusuario VALUES (" + str(idusuario) + ", '" + username + "', '" + dtnasc + "', '" + sexo +  "')"
                #print(sqlinsertdados)
                cursor.execute(sqlinsertdados)
                mysql.connection.commit()
                msg = 'Usuário cadastrado com sucesso!'
                #return render_template('registrar.html', msg=msg)
                return render_template("index.html")
        else :
            msg = 'As senhas não estão iguais'
    elif request.method == 'POST':
        msg = 'Por favor, preencha os dados'
    return render_template('registrar.html', msg = msg)


if __name__ == "__main__":
    app.run(debug=True)
