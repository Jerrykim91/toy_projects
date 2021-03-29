$(function(){               
    // string을 그대로 받으면 에러가 나니까 replace로 문자를 제외한 나머지 것들을 공백처리
    var str1 = '{{xlist}}'
    str1 = str1.replace(/&#x27;/gi, "'");
    str1 = str1.replace(/&#39;/gi, "'");
    
    var xlist = eval(str1)  //python 문자를 script 배열로 변환
    xlist.unshift('x_CountryName')
    //xlist.unshift('x');
    console.log(xlist)

    var ylist =eval('{{ylist}}')
    //obj.unshift('TOP10 GDP');
    ylist.unshift('{{how_many}}');

    console.log(ylist)
    
    // 그래프 구현
    // 차트의 x축, y축의 값을 결정
    var chart = c3.generate({
        bindto: '#chart',
        data: {
            x: 'x_CountryName',
            y: '{{how_many}}',
            columns: [
                xlist,
                ylist
            ],
           type: 'bar',
            colors: {
                '{{how_many}}': '#0000ff'
            }
        },

        // 현재 x축의 값을 결정
        axis: { 
            // x축의 높이를 결정
            x: {
            // type 을 카테고리로 해야 문자열이 나온다 안 하면 Error
                type : 'category',
                height: 80,
            //     tick: {
            //         values: [1960, 1965, 1970, 1975, 1980, 1985,1990,1995,2000,2005,2010,2015,2018]
            //     }
            },

            // y축의 범위 결정 및 라벨 제목 설정
            y: { 
                label : 'GDP (Current USD)',
                tick  : {
            // y축의 포맷 설정 ($,d)
                    format: d3.format("$,d"),
                }    
                // max: 30000000000000,
                // min: -100,
            }
        },
        size: {
            width: 1800,
            height: 700
        }
        // 그리드의 범위 지정
        // regions: [  
        //     {start:1979, end:1980, class:'foo'},
        //     {start:1980, end:1983, class:'foo1'}
        // ]
        // 차트의 크기 설정
    });
    setTimeout(function () {
    chart.resize({height:700, width:1600})
    }, 1000);
    //     // 그리드 설정
    // setTimeout(function () {
    //     chart.xgrids([
    //             {value: 1973, text: '제1차 석유파동(1973)'}, 
    //             {value: 1980, text: '제2차 석유파동(1979~1980)'}, 
    //             {value: 1983, text: '유럽 경기침체(1980~1983)'}, 
    //             {value: 1985, text: '플라자 합의(1985)'}, 
    //             {value: 1994, text: '일본 버블경제 붕괴(1994)'},
    //             {value: 1997, text: 'IMF(1997)'},
    //             {value: 2007, text: '서브프라임 모기지 사태(2007)'},
    //             {value: 2011, text: '동일본 대지진(2011)'},
    //             {value: 2016, text: '브렉시트(2016)'},
    //             {value: 2018, text: '현재'}
                
    //         ]);
    // }, 500);
})


$("#search1").click(function(){
    if ($('#country_name').val() == "" || $('#year1').val() == "" ){
        alert('정확한 값을 입력해주세요 = 나라명과 연도 ')
        $("#country_name").focus();
        return false;
    }   
    else {
        
           $('#form1').submit()
    }
})  

$("#search2").click(function(){
    if ($('#how_many').val() == "" || $('#year2').val() == "" ){
        alert('정확한 값을 입력해주세요 = 년도와 1위 나라수 ')
        $("#how_many").focus();
        return false;
    }   
    else {
           $('#form2').submit()

    }
}) 