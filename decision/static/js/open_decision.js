const loda = document.querySelectorAll("#r_time")
const burn = document.querySelectorAll("#g_list")


function conv_date(a){
    
    var m_list = a.split(' ');
    if (m_list[1] == "января") {
        month = "01";
      } 
      
    else if (m_list[1] == "февраля") {
        month = "02";
      } 
    

      else if (m_list[1] == "марта") {
        month = "03";
      } 
      else if (m_list[1] == "апреля") {
        month = "04";
      } 
      else if (m_list[1] == "мая") {
        month = "05";
      } 
      else if (m_list[1] == "июня") {
        month = "06";
      } 
      else if (m_list[1] == "июля") {
        month = "07";
      } 
      else if (m_list[1] == "августа") {
        month = "08";
      } 
      else if (m_list[1] == "сентября") {
        month = "09";
      } 
      else if (m_list[1] == "октября") {
        month = "10";
      } 
      else if (m_list[1] == "ноября") {
        month = "11";
      } 

      else if (m_list[1] == "декабря") {
        month = "12";
      } 

      let date2 = new Date(m_list[2]+'-'+month+'-'+m_list[0])
    
    return date2
    

}



//console.log(burn.querySelector("#r_status").textContent)

for(let r_date of burn){
    let st = r_date.querySelector("#r_status").textContent
    let dta = r_date.querySelector("#r_time").textContent

    

    let var_1 =  parseFloat(((conv_date(dta)) - new Date())/86400000)
    console.log(var_1)
    if(
    var_1 < (-0.5)
    &&
    st === "Активный "
    )
    r_date.classList.add("rem_0");


    else if(
        var_1 < 3
        &&
        var_1 > 1

        &&
        st === "Активный"
        )
        r_date.classList.add("rem_3");



    else if(
            var_1 > -0.5
            &&
            var_1 < 1
           // &&
           // st === "Активный"
            )
            r_date.classList.add("rem_1");

    

   
}








