from flask import Flask, flash, redirect, render_template, request, url_for,jsonify, Response
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import io
import xlwt
import pymysql

app= Flask(__name__)
app.secret_key="sistemabd"
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)


#Rutas de inicio
@app.route('/')
def login():
    return render_template("/login.html")

@app.route('/inicio')
def inicio():
    return render_template("recursoshumanos/inicio.html")

@app.route('/iniciocandidato')
def iniciocandidato():
    return render_template("recursoshumanos/iniciocandidato.html")

@app.route('/logout')
def logout():
        return redirect('/')


#Login
@app.route('/ingresar',  methods = ['POST', 'GET'])
def ingresar():  

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor2=conn.cursor()
    if request.method == 'POST':
        singup=request.form
        _nombre=singup['nombre']
        _password=singup['password']
        cursor.execute("SELECT usuarios.idusuario, usuarios.nombre, usuarios.password,tipousuario.nombretipo FROM usuarios INNER JOIN tipousuario ON usuarios.idtipo = tipousuario.idtipo WHERE usuarios.nombre='"+_nombre+"' and password='"+_password+"';")
        data=cursor2.execute("SELECT usuarios.idusuario, usuarios.nombre, usuarios.password,tipousuario.nombretipo FROM usuarios INNER JOIN tipousuario ON usuarios.idtipo = tipousuario.idtipo WHERE usuarios.nombre='"+_nombre+"' and tipousuario.nombretipo='Administrador'")
        r=cursor.fetchall()
        count=cursor.rowcount
    if count==1:
            s=cursor2.fetchall()
            count=cursor2.rowcount
            if count==1:
                return redirect('inicio')
            else:
                return redirect('iniciocandidato')
    else:
        flash("Usuario no encontrado")
        return render_template("login.html")


#CRUD DE COMPETENCIAS
@app.route('/indexcomp')
def indexcomp():
    sql="SELECT * FROM `competencias`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    competencias=cursor.fetchall()
    print(competencias)

    conn.commit()
    return render_template('recursoshumanos/competencias/indexcomp.html',competencias=competencias)

@app.route('/destroycomp/<int:id>')
def destroycomp(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM `competencias` WHERE Idcompetencia =%s",(id))
    conn.commit()
    return redirect('/indexcomp')

@app.route('/editcomp/<int:id>')
def editcomp(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * from `competencias` WHERE Idcompetencia =%s",(id))
    competencias=cursor.fetchall()
    print(competencias)

    
    conn.commit()
    return render_template('recursoshumanos/competencias/editcomp.html',competencias=competencias)

@app.route('/updatecomp', methods=['POST'])
def updatecomp():
    _descripcion=request.form['txtDescripcion']
    _estado=request.form['txtEstado']

    id=request.form['txtID']
    sql="UPDATE `competencias` SET `Descripcion`=%s, `estado`=%s WHERE Idcompetencia=%s;"
    datos=(_descripcion,_estado,id)
    conn=mysql.connect() 
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/indexcomp')

@app.route('/createcomp')
def createcomp():
    return render_template ('recursoshumanos/competencias/createcomp.html')

@app.route('/storecomp', methods=['POST'])
def storecomp():
    _descripcion=request.form['txtDescripcion']
    _estado=request.form['txtEstado']

    if _descripcion=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('createcomp'))
        
    sql="INSERT INTO `competencias` (`Idcompetencia`, `Descripcion`, `estado`) VALUES (NULL, %s, %s);"

    datos=(_descripcion,_estado)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/indexcomp')

#CRUD DE IDIOMAS

@app.route('/indexidioma')
def indexidioma():
    sql="SELECT * FROM `idiomas`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    idiomas=cursor.fetchall()
    print(idiomas)
    conn.commit()
    return render_template('/recursoshumanos/idiomas/indexidioma.html', idiomas=idiomas)

@app.route('/destroyidioma/<int:id>')
def destroyidioma(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM `idiomas` WHERE Ididioma =%s",(id))
    conn.commit()
    return redirect('/indexidioma')

@app.route('/editidioma/<int:id>')
def editidioma(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * from `idiomas` WHERE Ididioma =%s",(id))
    idiomas=cursor.fetchall()
    print(idiomas)
    conn.commit()
    return render_template('recursoshumanos/idiomas/editidioma.html',idiomas=idiomas)

@app.route('/updateidioma', methods=['POST'])
def updateidioma():
    _Nombre=request.form['txtNombre']
    _estado=request.form['txtEstado']

    id=request.form['txtID']
    sql="UPDATE `idiomas` SET `Nombre`=%s, `estado`=%s WHERE Ididioma=%s;"

    datos=(_Nombre,_estado,id)
    conn=mysql.connect() 
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/indexidioma')

@app.route('/createidioma', methods=['GET', 'POST'])
def createidioma():
    sql="SELECT * FROM `idiomas`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    idiomas = cursor.fetchall()
    conn.commit()
    return render_template ('recursoshumanos/idiomas/createidioma.html', idiomas=idiomas)
    
@app.route('/storeidioma', methods=['POST'])
def storeidioma():
    _Nombre=request.form['txtNombre']
    _estado=request.form['txtEstado']

    if _Nombre=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('createidioma'))
        
    sql="INSERT INTO `idiomas` (`Ididioma`, `Nombre`, `estado`) VALUES (NULL, %s, %s);"
    datos=(_Nombre,_estado)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/indexidioma')

#CRUD DE CANDIDATOS

@app.route('/indexcand')
def indexcand():
    sql="SELECT candidatos.Idcandidato, candidatos.Cedula, candidatos.Nombre, puestos.Nombre, candidatos.Idcompetencia, candidatos.Idcapacitacion, candidatos.Salariodeseado, candidatos.Recomendado FROM candidatos INNER JOIN puestos on candidatos.Idpuesto = puestos.Idpuesto WHERE NOT EXISTS (SELECT * FROM empleados WHERE empleados.Idcandidato = candidatos.Idcandidato);"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    candidatos=cursor.fetchall()
    print(candidatos)

    conn.commit()
    return render_template('/recursoshumanos/candidatos/indexcand.html', candidatos=candidatos)

@app.route('/destroycand/<int:id>')
def destroycand(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM `candidatos` WHERE Idcandidato =%s",(id))
    conn.commit()
    return redirect('/indexcand')

@app.route('/editcand/<int:id>')
def editcand(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * from `candidatos` WHERE Idcandidato =%s",(id))
    candidatos=cursor.fetchall()
    print(candidatos)
    sql="SELECT candidatos.Idcandidato, candidatos.Cedula, candidatos.Nombre, puestos.Nombre, candidatos.Ididioma, candidatos.Salariodeseado, candidatos.Recomendado FROM candidatos INNER JOIN puestos on candidatos.Idpuesto = puestos.Idpuesto;" 
    sql2="SELECT * FROM `puestos` WHERE estado='Activo'"
    sql3="SELECT * FROM `competencias` WHERE estado='Activo'"
    sql4="SELECT * FROM `capacitaciones`"
    sql5="SELECT * FROM `idiomas` WHERE estado='Activo'"

    cursor=conn.connect()
    cursor=conn.cursor(DictCursor)
    cursor2=conn.cursor(DictCursor)
    cursor3=conn.cursor(DictCursor)
    cursor4=conn.cursor(DictCursor)
    cursor5=conn.cursor(DictCursor)

    cursor.execute(sql)
    cursor2.execute(sql2)
    cursor3.execute(sql3)
    cursor4.execute(sql4)
    cursor5.execute(sql5)

    candidato=cursor.fetchall()
    puestos=cursor2.fetchall()
    competencias=cursor3.fetchall()
    capacitaciones=cursor4.fetchall()
    idiomas=cursor5.fetchall()
    conn.commit()
    return render_template('/recursoshumanos/candidatos/editcand.html',candidatos=candidatos, candidato = candidato, puestos = puestos, competencias=competencias, capacitaciones=capacitaciones, idiomas=idiomas)

@app.route('/updatecand', methods=['POST'])
def updatecand():
    _Cedula=request.form['txtCedula']
    _Nombre=request.form['txtNombre']
    _puesto=request.form['txtpuesto']
    _idioma=request.form.getlist('txtidioma')
    _Competencia=request.form.getlist('txtcompetencia')
    _capacitaciones=request.form.getlist('txtcapacitaciones')    
    _Salariodeseado=request.form['txtSalariodeseado']
    _Recomendado=request.form['txtRecomendado']
    
    conn=mysql.connect()
    cursor=conn.cursor()

    if _Nombre=='' or _Cedula=='' or _Salariodeseado=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('createcand'))

    cursor.execute("SELECT `Cedula` FROM `candidatos`WHERE Cedula='"+_Cedula+"';")
    count=cursor.rowcount
    if count==1:
        flash('La cedula insertada ya se encuentra registrada')
        return redirect(url_for('createcand'))
            
    id=request.form['txtID']
    sql="UPDATE `candidatos` SET `Cedula`=%s, `Nombre`=%s, `Idpuesto`=%s, `Ididioma`=%s, `Idcompetencia`=%s, `Idcapacitacion`=%s,`Salariodeseado`=%s,`Recomendado`=%s WHERE Idcandidato=%s;"
   
    a = _Competencia
    listacompetencia = ' '.join(map(str, a))
    
    b = _idioma
    listaidioma = ' '.join(map(str, b))

    c = _capacitaciones
    listacapacitaciones = ' '.join(map(str, c))

    
    datos=(_Cedula, _Nombre, _puesto, listaidioma, listacompetencia, listacapacitaciones, _Salariodeseado,_Recomendado ,id)
    cursor=conn.cursor(DictCursor)
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/indexcand')

@app.route('/createcand')
def createcand():
    sql="SELECT * FROM `puestos` WHERE estado='Activo'"
    sql2="SELECT * FROM `competencias` WHERE estado='Activo'"
    sql3="SELECT * FROM `idiomas` WHERE estado='Activo'"
    sql4="SELECT * FROM `capacitaciones`"
    sql5="SELECT * FROM `experiencialaboral`"

    conn=mysql.connect()
    cursor=conn.connect()

    cursor=conn.cursor(DictCursor)
    cursor2=conn.cursor(DictCursor)
    cursor3=conn.cursor(DictCursor)
    cursor4=conn.cursor(DictCursor)
    cursor5=conn.cursor(DictCursor)


    cursor.execute(sql)
    cursor2.execute(sql2)
    cursor3.execute(sql3)
    cursor4.execute(sql4)
    cursor5.execute(sql5)


    puestos=cursor.fetchall()
    competencias=cursor2.fetchall()
    idiomas=cursor3.fetchall()
    capacitaciones=cursor4.fetchall()
    experiencia=cursor5.fetchall()
    conn.commit()
    return render_template ('recursoshumanos/candidatos/createcand.html', puestos = puestos, competencias=competencias, idiomas=idiomas, capacitaciones=capacitaciones, experiencia=experiencia)

@app.route('/storecand', methods=['POST', 'GET'])
def storecand():
 if request.method == 'POST':   
    singup=request.form
    _Cedula=singup['txtCedula']
    _Nombre=request.form['txtNombre']
    _puesto=request.form['txtpuesto']
    _idioma=request.form.getlist('txtidioma')
    _Salariodeseado=request.form['txtSalariodeseado']
    _Competencia=request.form.getlist('txtCompetencia')
    _capacitaciones=request.form.getlist('txtcapacitaciones')
    _experiencia=request.form.getlist('txtexperiencia')
    _Recomendado=request.form['txtRecomendado']

    conn=mysql.connect()
    cursor=conn.cursor()

    if _Nombre=='' or _Cedula=='' or _Salariodeseado=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('createcand'))

    cursor.execute("SELECT `Cedula` FROM `candidatos`WHERE Cedula='"+_Cedula+"';")
    count=cursor.rowcount
    if count==1:
        flash('La cedula insertada ya se encuentra registrada')
        return redirect(url_for('createcand'))
            

    sql="INSERT INTO `candidatos` (`Idcandidato`,`Cedula`,`Nombre`,`Idpuesto`,`Ididioma`,`Salariodeseado`, `Idcompetencia`,`Idcapacitacion`,`Idexperiencia`,`Recomendado`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    a = _Competencia
    listacompetencia = ' '.join(map(str, a))
    
    b = _idioma
    listaidioma = ' '.join(map(str, b))

    c = _capacitaciones
    listacapacitaciones = ' '.join(map(str, c))

    d = _experiencia
    listaexperiencia = ' '.join(map(str, d))

    datos=(_Cedula, _Nombre, _puesto, listaidioma, _Salariodeseado, listacompetencia, listacapacitaciones, listaexperiencia, _Recomendado)
    cursor=conn.cursor(DictCursor)
    cursor.execute(sql,datos)
    conn.commit()
    conn.close()
    return redirect('/indexcand')

@app.route('/buscarcand')
def buscarcand():
    sql="SELECT candidatos.Idcandidato, candidatos.Cedula, candidatos.Nombre, puestos.Nombre, candidatos.Idcompetencia, candidatos.Idcapacitacion, candidatos.Salariodeseado, candidatos.Recomendado FROM candidatos INNER JOIN puestos on candidatos.Idpuesto = puestos.Idpuesto WHERE NOT EXISTS (SELECT * FROM empleados WHERE empleados.Idcandidato = candidatos.Idcandidato);"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    candidatos=cursor.fetchall()
    print(candidatos)

    conn.commit()
    return render_template('/recursoshumanos/candidatos/buscarcand.html', candidatos=candidatos)

#CRUD DE Empleados

@app.route('/indexempleado')
def indexempleado():
    sql="SELECT empleados.Idempleado, candidatos.Nombre, candidatos.Cedula, empleados.Fechaingreso, departamento.Nombre, puestos.Nombre,candidatos.Salariodeseado, empleados.estado FROM `empleados` INNER JOIN candidatos on empleados.Idcandidato = candidatos.Idcandidato INNER JOIN puestos on candidatos.Idpuesto = puestos.Idpuesto INNER JOIN departamento on puestos.Iddepartamento = departamento.Iddepartamento;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    print(empleados)
    conn.commit()
    return render_template('/recursoshumanos/Empleados/indexempleado.html', empleados=empleados)

@app.route('/reporteempleado')
def reporteempleado():
    sql="SELECT empleados.Idempleado, candidatos.Nombre, candidatos.Cedula, empleados.Fechaingreso, departamento.Nombre, puestos.Nombre,candidatos.Salariodeseado, empleados.estado FROM `empleados` INNER JOIN candidatos on empleados.Idcandidato = candidatos.Idcandidato INNER JOIN puestos on candidatos.Idpuesto = puestos.Idpuesto INNER JOIN departamento on puestos.Iddepartamento = departamento.Iddepartamento;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    print(empleados)
    conn.commit()
    return render_template('/recursoshumanos/Empleados/reporteempleado.html', empleados=empleados)


@app.route("/range",methods=["POST","GET"])
def range(): 
    conn=mysql.connect()
    cursor=conn.cursor()
    if request.method == 'POST':
        From = request.form['From']
        to = request.form['to']
        print(From)
        print(to)
        sql="SELECT empleados.Idempleado, candidatos.Nombre, candidatos.Cedula, empleados.Fechaingreso, departamento.Nombre, puestos.Nombre,candidatos.Salariodeseado, empleados.estado FROM `empleados` INNER JOIN candidatos on empleados.Idcandidato = candidatos.Idcandidato INNER JOIN puestos on candidatos.Idpuesto = puestos.Idpuesto INNER JOIN departamento on puestos.Iddepartamento = departamento.Iddepartamento WHERE empleados.Fechaingreso BETWEEN '{}' AND '{}'".format(From,to)
        cursor.execute(sql)
        rango = cursor.fetchall()
        return jsonify({'htmlresponse': render_template('/recursoshumanos/Empleados/indexempleado.html', rango=rango)})


@app.route('/contratar/<int:id>')
def contratar(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO `empleados` (`Idempleado`, `Idcandidato`, `Fechaingreso`, `estado`) VALUES (Null,%s,now(),'Activo');",(id))
    sql="UPDATE `puestos` SET `estado`='Inactivo' WHERE Idpuesto in (SELECT puestos.Idpuesto FROM candidatos INNER JOIN puestos on candidatos.Idpuesto = puestos.Idpuesto INNER JOIN empleados on candidatos.Idcandidato=empleados.Idcandidato WHERE candidatos.Idcandidato= empleados.Idcandidato)"
    cursor.execute(sql)
    conn.commit()
    return redirect('/reporteempleado')

@app.route('/download/report/excel', methods=["POST","GET"])
def download_report():
  conn = mysql.connect()
  cursor=conn.cursor(DictCursor)
  if request.method == 'POST':
    reporte=request.form
    From = reporte['From']
    to = reporte['to']
  cursor.execute("SELECT empleados.Idempleado as id, candidatos.Nombre as nombre, candidatos.Cedula as cedula, empleados.Fechaingreso as fecha, departamento.Nombre as departamento, puestos.Nombre as puesto,candidatos.Salariodeseado as salario, empleados.estado as estado FROM `empleados` INNER JOIN candidatos on empleados.Idcandidato = candidatos.Idcandidato INNER JOIN puestos on candidatos.Idpuesto = puestos.Idpuesto INNER JOIN departamento on puestos.Iddepartamento = departamento.Iddepartamento")
  result = cursor.fetchall()
  #output in bytes
  output = io.BytesIO()
  #create WorkBook object
  workbook = xlwt.Workbook()
  #add a sheet
  sh = workbook.add_sheet('Employee Report')
   
  #add headers
  sh.write(0, 0, 'ID')
  sh.write(0, 1, 'Emp First Name')
  sh.write(0, 2, 'Emp Last Name')
  sh.write(0, 3, '1')
  sh.write(0, 4, '2')
  sh.write(0, 5, '3')
  sh.write(0, 6, '4')
  sh.write(0, 7, '5')

   
  idx = 0
  for row in result:
   sh.write(idx+1, 0, str(row['id']))
   sh.write(idx+1, 1, row['nombre'])
   sh.write(idx+1, 2, row['cedula'])
   sh.write(idx+1, 3, row['fecha'])
   sh.write(idx+1, 4, str(row['departamento']))
   sh.write(idx+1, 5, row['puesto'])
   sh.write(idx+1, 6, row['salario'])
   sh.write(idx+1, 7, row['estado'])
   idx += 1
   
  workbook.save(output)
  output.seek(0)
   
  return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=employee_report.xls"})

#CRUD DE CAPACITACIONES

@app.route('/indexcapa')
def indexcapa():
    sql="SELECT * FROM `capacitaciones`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    capacitaciones=cursor.fetchall()
    print(capacitaciones)

    conn.commit()
    return render_template('/recursoshumanos/capacitaciones/indexcapa.html', capacitaciones=capacitaciones)

@app.route('/destroycapa/<int:id>')
def destroycapa(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM `capacitaciones` WHERE Idcapacitacion =%s",(id))
    conn.commit()
    return redirect('/indexcapa')

@app.route('/editcapa/<int:id>')
def editcapa(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * from `capacitaciones` WHERE Idcapacitacion =%s",(id))
    capacitaciones=cursor.fetchall()
    print(capacitaciones)
    conn.commit()
    return render_template('recursoshumanos/capacitaciones/editcapa.html',capacitaciones=capacitaciones)

@app.route('/updatecapa', methods=['POST'])
def updatecapa():
    _Descripcion=request.form['txtDescripcion']
    _Nivel=request.form['txtNivel']
    _Fechadesde=request.form['txtFechadesde']
    _Fechahasta=request.form['txtFechahasta']
    _Institucion=request.form['txtInstitucion']

    id=request.form['txtID']
    sql="UPDATE `capacitaciones` SET `Descripcion`=%s, `Nivel`=%s, `Fechadesde`=%s, `Fechahasta`=%s, `Institucion`=%s WHERE Idcapacitacion=%s;"

    datos=(_Descripcion,_Nivel, _Fechadesde, _Fechahasta, _Institucion,id)
    conn=mysql.connect() 
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/indexcapa')

@app.route('/createcapa')
def createcapa():
    return render_template ('recursoshumanos/capacitaciones/createcapa.html')

@app.route('/storecapa', methods=['POST'])
def storecapa():
    _Descripcion=request.form['txtDescripcion']
    _Nivel=request.form['txtNivel']
    _Fechadesde=request.form['txtFechadesde']
    _Fechahasta=request.form['txtFechahasta']
    _Institucion=request.form['txtInstitucion']

    if _Descripcion=='' or _Nivel=='' or _Institucion=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('createcapa'))
        
    sql="INSERT INTO `capacitaciones` (`Idcapacitacion`, `Descripcion`, `Nivel`, `Fechadesde`, `Fechahasta`, `Institucion`) VALUES (NULL, %s, %s, %s, %s, %s);"

    datos=(_Descripcion,_Nivel, _Fechadesde, _Fechahasta, _Institucion)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/indexcapa')


#CRUD DE PUESTOS

@app.route('/indexpuesto')
def indexpuesto():
    sql="SELECT puestos.Idpuesto,puestos.Nombre,puestos.Riesgo,departamento.Nombre,puestos.Salariominimo,puestos.Salariomaximo,puestos.estado FROM (puestos INNER JOIN departamento on puestos.Iddepartamento = departamento.Iddepartamento);" 
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    puestos=cursor.fetchall()
    print(puestos)

    conn.commit()
    return render_template('/recursoshumanos/puestos/indexpuesto.html', puestos=puestos)

@app.route('/destroypuesto/<int:id>')
def destroypuesto(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM `puestos` WHERE Idpuesto =%s",(id))
    conn.commit()
    return redirect('/indexpuesto')

@app.route('/editpuesto/<int:id>')
def editpuesto(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * from `puestos` WHERE Idpuesto =%s",(id))
    puestos=cursor.fetchall()
    print(puestos)
    sql="SELECT puestos.Idpuesto,puestos.Nombre,puestos.Riesgo,departamento.Nombre,puestos.Salariominimo,puestos.Salariomaximo,puestos.estado FROM (puestos INNER JOIN departamento on puestos.Iddepartamento = departamento.Iddepartamento);" 
    sql2="SELECT * FROM `departamento`"
    cursor=conn.connect()
    cursor=conn.cursor(DictCursor)
    cursor2=conn.cursor(DictCursor)
    cursor.execute(sql)
    cursor2.execute(sql2)
    puesto=cursor.fetchall()
    departamento=cursor2.fetchall()
    conn.commit()
    return render_template('recursoshumanos/puestos/editpuesto.html',puestos=puestos, puesto=puesto, departamento=departamento)

@app.route('/updatepuesto', methods=['POST'])
def updatepuesto():
    _Nombre=request.form['txtNombre']
    _Riesgo=request.form['txtRiesgo']
    _Departamento=request.form['txtDepartamento']
    _Salariominimo=request.form['txtSalariominimo']
    _Salariomaximo=request.form['txtSalariomaximo']
    _Estado=request.form['txtEstado']

    id=request.form['txtID']
    sql="UPDATE `puestos` SET `Nombre`=%s, `Riesgo`=%s, `Iddepartamento`=%s, `Salariominimo`=%s, `Salariomaximo`=%s,`estado`=%s WHERE Idpuesto=%s;"

    datos=(_Nombre,_Riesgo,_Departamento,_Salariominimo,_Salariomaximo,_Estado,id)
    conn=mysql.connect() 
    cursor=conn.cursor()
    cursor=conn.cursor(DictCursor)
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/indexpuesto')

@app.route('/createpuesto')
def createpuesto():
    sql="SELECT * FROM `departamento`"
    conn=mysql.connect()
    cursor=conn.connect()
    cursor=conn.cursor(DictCursor)
    cursor.execute(sql)
    departamento=cursor.fetchall()
    conn.commit()
    return render_template ('recursoshumanos/puestos/createpuesto.html', departamento=departamento)

@app.route('/storepuesto', methods=['Get','POST'])
def storepuesto():
    _Nombre=request.form['txtNombre']
    _Riesgo=request.form['txtRiesgo']
    _Departamento=request.form['txtDepartamento']
    _Salariominimo=request.form['txtSalariominimo']
    _Salariomaximo=request.form['txtSalariomaximo']
    _Estado=request.form['txtEstado']

    if _Nombre=='' or _Salariominimo=='' or _Salariomaximo=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('createpuesto'))
        
    sql="INSERT INTO `puestos` (`Idpuesto`, `Nombre`, `Riesgo`, `Iddepartamento`, `Salariominimo`, `Salariomaximo` ,`estado`) VALUES (NULL, %s, %s, %s, %s, %s, %s);"
    datos=(_Nombre, _Riesgo, _Departamento, _Salariominimo, _Salariomaximo,_Estado)
    conn=mysql.connect()
    cursor=conn.cursor(DictCursor)
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/indexpuesto')


#CRUD DE EXPERIENCIA LABORAL

@app.route('/indexexpe')
def indexexpe():
    sql="SELECT * FROM `experiencialaboral`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    experiencialaboral=cursor.fetchall()
    print(experiencialaboral)

    conn.commit()
    return render_template('/recursoshumanos/experiencia/indexexpe.html', experiencialaboral=experiencialaboral)

@app.route('/destroyexpe/<int:id>')
def destroyexpe(id):
    conn=mysql.connect()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM `experiencialaboral` WHERE Idexperiencia =%s",(id))
    conn.commit()
    return redirect('/indexexpe')

@app.route('/editexpe/<int:id>')
def editexpe(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * from `experiencialaboral` WHERE Idexperiencia =%s",(id))
    experiencialaboral=cursor.fetchall()
    print(experiencialaboral)
    conn.commit()
    return render_template('recursoshumanos/experiencia/editexpe.html',experiencialaboral=experiencialaboral)

@app.route('/updateexpe', methods=['POST'])
def updateexpe():
    _Empresa=request.form['txtEmpresa']
    _Puesto=request.form['txtPuesto']
    _Fechadesde=request.form['txtFechadesde']
    _Fechahasta=request.form['txtFechahasta']
    _Salario=request.form['txtSalario']

    id=request.form['txtID']
    sql="UPDATE `experiencialaboral` SET `Empresa`=%s, `Puesto`=%s, `Fechadesde`=%s, `Fechahasta`=%s, `Salario`=%s WHERE Idexperiencia=%s;"

    datos=(_Empresa, _Puesto, _Fechadesde, _Fechahasta, _Salario,id)
    conn=mysql.connect() 
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/indexexpe')

@app.route('/createexpe')
def createexpe():
    return render_template ('recursoshumanos/experiencia/createexpe.html')

@app.route('/storeexpe', methods=['POST'])
def storeexpe():
    _Empresa=request.form['txtEmpresa']
    _Puesto=request.form['txtPuesto']
    _Fechadesde=request.form['txtFechadesde']
    _Fechahasta=request.form['txtFechahasta']
    _Salario=request.form['txtSalario']

    if _Empresa=='' or _Puesto=='' or _Salario=='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('createexpe'))
        
    sql="INSERT INTO `experiencialaboral` (`Idexperiencia`, `Empresa`, `Puesto`, `Fechadesde`, `Fechahasta`, `Salario`) VALUES (NULL, %s, %s, %s, %s, %s);"

    datos=(_Empresa, _Puesto, _Fechadesde, _Fechahasta, _Salario)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/indexexpe')

if __name__ == '__main__':
    app.run(debug=True)
