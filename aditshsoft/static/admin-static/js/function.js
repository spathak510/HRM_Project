function clearText(thefield) {
  if (thefield.defaultValue==thefield.value) { thefield.value = "" }
} 
function replaceText(thefield) {
  if (thefield.value=="") { thefield.value = thefield.defaultValue }
}


var s='';
function sub_link_show(sid,cid)
{
  s=document.getElementById(cid).className
  document.getElementById(sid).style.display='block';
  document.getElementById(cid).className='sel';
}

function sub_link_hide(sid,cid)
{
  document.getElementById(sid).style.display='none';  

  if(s=='select')

  {
   document.getElementById(cid).className=s;
  }

  else
  {
   document.getElementById(cid).className='';
  }
}

