function pad(n, width, z) {
    z = z || '0';
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}
function datef(fstr, format){
    let fec=new Date(fstr)
    if(typeof(format)=='undefined'){
        return pad(fec.getDate(),2)+'/'+pad(fec.getMonth()+1,2)+'/'+fec.getFullYear()+' '+pad(fec.getHours(),2)+':'+pad(fec.getMinutes(),2)+':'+pad(fec.getSeconds(),2)
    }else{
        return pad(fec.getDate(),2)+'/'+pad(fec.getMonth()+1,2)+'/'+fec.getFullYear()
    }


}


function descMinutos(minutos){
	var desc = ''; var dias=0; var horas=0;
	dias = Math.floor(minutos / 1440);
	minutos = minutos - dias * 1440 ;
	horas = Math.floor(minutos / 60);
	minutos = minutos - horas * 60 ;
	if( dias >= 1 ){
		desc += dias + ' día/s ';
	}
	if( horas >= 1 ){
		desc += horas + ' hs ';
	}
	if( minutos >= 1 ){
		desc += minutos + ' min';
	}
	return desc;
}
dtptooltips= {
    today: 'Hoy',
    clear: 'Limpiar selección',
    close: 'Cerrar',
    selectMonth: 'Seleccionar mes',
    prevMonth: 'Mes anterior',
    nextMonth: 'Mes siguiente',
    selectYear: 'Seleccionar año',
    prevYear: 'Año anterior',
    nextYear: 'Año siguiente',
    selectDecade: 'Seleccionar década',
    prevDecade: 'Década anterior',
    nextDecade: 'Década siguiente',
    prevCentury: 'Siglo anterior',
    nextCentury: 'Siglo siguiente',
    incrementHour: 'Incrementar hora',
    pickHour: 'Seleccionar hora',
    decrementHour:'Decrementar hora',
    incrementMinute: 'Incrementar minuto',
    pickMinute: 'Seleccionar ninuto',
    decrementMinute:'Decrementar minuto',
    incrementSecond: 'Incrementar segundo',
    pickSecond: 'Seleccionar segundo',
    decrementSecond:'Decrementar segundo'
}
dtpbuttons={
    showToday: true,
    showClear: true,
    showClose: true
}

// $(document).ready(function(){
    // getNavStat()
// })

function setNavStat(stat){
    // var estado
    // if(stat=='collapsed'){
    //     estado=0
    // }else{
    //     estado=1
    // }
    // $.ajax({
    //     url : '/inicio/navstat/'+estado,
    //     type: 'POST',
    // }).done(function(obj){
    // }).fail(function(resp){
    //     eval(resp.responseText);
    // })
}
function getNavStat(){
    $.ajax({
        url : '/inicio/navstat',
        type: 'GET',
        dataType:'json'
    }).done(function(obj){
        if(obj[0].stat==0){
            if ($('.hide-sidebar').length==0){
                $(".nav-toggle").click()
            }
        }
    }).fail(function(resp){
        eval(resp.responseText);
    })
}

function calcEdadAM(fnac){
    var dob=moment(fnac,'DD/MM/YYYY')
    var ahora=moment()
/*    var anios = ahora.diff(dob,'years')
    var meses = ahora.diff(dob,'months') - ahora.diff(dob,'years') * 12
  */

   var edad= ''
   var anios = ahora.diff(dob,'years')
   dob.add(anios, 'years');
   var meses = ahora.diff(dob,'months')
   dob.add(meses, 'months');
   var dias = ahora.diff(dob,'days')
    if(anios>0){
        edad += anios + ' año'+(anios>1?'s':'')
    }
    if(meses>0){
        edad += (edad==''?'':' y ') + meses + ' mes'+(meses>1?'es':'')
    }
    if(dias>0){
        edad += (edad==''?'':' y ') + dias + ' dia'+(dias>1?'s':'')
    }
    return edad
}

// $(document).on('mouseup touchend', function (e) {
//       var container = $('.bootstrap-datetimepicker-widget');
//     if (!container.is(e.target) && container.has(e.target).length === 0) {
//             container.parent().datetimepicker('hide');
//     }

// });

function detectMob() {
    const toMatch = [
        /Android/i,
        /webOS/i,
        /iPhone/i,
        /iPad/i,
        /iPod/i,
        /BlackBerry/i,
        /Windows Phone/i
    ];
    return toMatch.some((toMatchItem) => {
                return navigator.userAgent.match(toMatchItem);
    });
}
