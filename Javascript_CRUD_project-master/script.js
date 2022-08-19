var selectedLine = null;

function operate()          //입력폼의 값을 가져와 변수에 저장 후 추가or수정 함수를 실행 후 입력창 초기화
{		       
	if(errorCheck())
	{                 
		var foodData = readData();
		if(selectedLine == null)
		{
			addNewData(foodData);
		}else
		{
			updateData(foodData);
		}
		resetData();
	}	
}	

function readData()                  // 입력창에 입력된 값을 가져와 저장
{
	var foodData = [];
	foodData["foodName"] = document.getElementById("foodName").value;
	return foodData;
}

function addNewData(data)             // 행을 추가하여 저장된 입력값을 가져와 추가 + 수정버튼 생성
{
	var table = document.getElementById("foodList").getElementsByTagName('tbody')[0];
	var newLine = table.insertRow(table.length);
	cell1 = newLine.insertCell(0);
	cell1.innerHTML = data.foodName;
	cell2 = newLine.insertCell(1);
	cell2.innerHTML = `<input type="image" src="edit.png" width="30px" onclick="clickEdit(this)" value="수정">
						<input type="image" src="delete.png" width="30px" onclick="clickDelete(this)" value="삭제">
						<input type="image" src="picked.png" width="30px" onclick="picked(this)" value="찜">`;
}

function resetData()				// 입력창 초기화
{
	document.getElementById("foodName").value = "";
	selectedLine = null;
}

function clickEdit(td)              //메세지 출력후 해당 td값 입력창으로 가져옴
{
	var check = confirm("수정하시겠습니까?");
	if(check == true)
	{
		selectedLine = td.parentElement.parentElement;
		document.getElementById("foodName").value = selectedLine.cells[0].innerHTML;
	}
}

function updateData(foodData)          //해당 td값을 수정된 입력값으로 저장
{
	selectedLine.cells[0].innerHTML = foodData.foodName;
}

function clickDelete(td)					// 삭제 확인 메시지 출력 후 해당 열의 값 삭제
{
	if(confirm("삭제하시겠습니까?"))
	{
		line = td.parentElement.parentElement;
		document.getElementById("foodList").deleteRow(line.rowIndex);
		resetData();
	}
}

function errorCheck()						// 입력 창에 값이 없을 경우 경고문구 출력
{
	var writing_check = true;
	if(document.getElementById("foodName").value == "")
	{
		writing_check = false;
		document.getElementById("error").classList.remove("hide");
	}else {
		writing_check = true;
		if(!document.getElementById("error").classList.contains("hide"))
			document.getElementById("error").classList.add("hide");
	}
	return writing_check;
}

                                      /*입력값을 대문자로 모두 바꿈 (영어입력값의 경우)
                                        tr변수에 테이블속 tr 태그 획득
                                        td변수에 tr태그의 td 태그 획득 (tr의 갯수(길이만큼))
                                        tdata변수에 해당 td값을 넣고 tdata가 만약 입력값을 포함하면
                                        보이게끔 설정하고 포함하지 않는다면 안보이게 설정  */
function search(){
  var search_input = document.getElementById("search_foodName");
  var table = document.getElementById("foodList");
  filter = search_input.value.toUpperCase();
  var tr = document.getElementById("foodList").getElementsByTagName('tr');
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td") ; 
    for(j=0 ; j<td.length ; j++)
    {
      let tdata = td[j] ;
      if (tdata) {
        if (tdata.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
          break ; 
        } else {
          tr[i].style.display = "none";
        }
      } 
    }
  }
}

function picked(td)										// 찜 목록 추가
{
	var pickedLine = td.parentElement.parentElement;
  var pickedTable = document.getElementById("pickedList").getElementsByTagName('tbody')[0];
  var newPickedLine = pickedTable.insertRow(pickedTable.length);
  pickedCell1 = newPickedLine.insertCell(0);
  pickedCell1.innerHTML = pickedLine.cells[0].innerHTML; 
  pickedCell2 = newPickedLine.insertCell(1);
  pickedCell2.innerHTML = '<input type="image" src="delete.png" width="30px" onclick="pickedDelete(this)" value="삭제">'
}

function pickedDelete(td)								// 찜 목록에서 삭제 기능 추가
{
	if(confirm("찜 목록에서 삭제하시겠습니까?"))
	{
		pickedLine = td.parentElement.parentElement;
		document.getElementById("pickedList").deleteRow(pickedLine.rowIndex);
	}
}