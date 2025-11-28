function windowSize(){
	// We execute the same script as before
	let vh = window.innerHeight * 0.01;
	document.documentElement.style.setProperty('--vh', `${vh}px`);
}

$(window).load(windowSize);
$(window).resize(windowSize);
$(window).on('load resize',windowSize);


function getCookie(name) {
	var matches = document.cookie.match(new RegExp(
		"(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") + "=([^;]*)"
	));
	return matches ? decodeURIComponent(matches[1]) : undefined;
}

function writeCookie(name, value, days) {
	var expires = "";
    
    if(days) 
	{
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    }

	document.cookie = name + "=" + value + expires + "; path=/";

	return value;
}



// Calculator v2 Sum
function SumRez () 
{
	var vk      = document.getElementById("clt_vk").value;		
	var pskidka = document.getElementById("clt_pskidka").value;		
	var qq      = $(".clt_km--js").val();

	var vid    = $('#clt_vid_' + vk ).val(); if (!!vid){ } else { vid = 0; }
	var skidka = $('#clt_vid_' + vk + ' option:selected').data("skidka"); if (!!skidka){ } else { skidka = 0; }
	
	var price  = $('#clt_tip_' + vk + '_' + vid + ' option:selected').data("price"); if (!!price){ } else { price = 0; }
	var km     = $('#clt_tip_' + vk + '_' + vid + ' option:selected').data("km"); if (!!km){ } else { km = 0; }
	var tip    = $('#clt_tip_' + vk + '_' + vid + ' option:selected').val(); if (!!tip){ } else { tip = 0; }
	
	$("#clt_tip").val(tip); 
	
	var koleso_qq = $('#clt_koleso').val(); if (!!koleso_qq){ } else { koleso_qq = 0; }	
	var koleso_pr = $('#clt_koleso').data("price"); if (!!koleso_pr){ } else { koleso_pr = 0; }
	
	var predzakaz    = $('#clt_predzakaz:checked').val(); if (!!predzakaz){ } else { predzakaz = 0; }	
	var predzakaz_pr = $('#clt_predzakaz').data("price"); if (!!predzakaz_pr){ } else { predzakaz_pr = 0; }
	
	var uvedomlenie = 0;

	$('.clt_tip--js').addClass("d-none");
	$('.clt_tip_' + vk + '_' + vid + '--js').removeClass("d-none");
	
	var sum   = price;
	var minus = 0;
	var old   = 0;
	
	sum += km * qq;
	
	if ( pskidka > skidka )
	{
		skidka = pskidka;
	}
	
	if ( ( qq >= 500 ) && ( skidka < 10 ) )
	{
		skidka = 10;
	}
	

	
	
	if ( vk == 1 ) 
	{
		var dop_1_1 = $('#clt_dop_1_1:checked').val(); if (!!dop_1_1){ } else { dop_1_1 = 0; }
		var dop_1_1_pr = $('#clt_dop_1_1').data("price"); if (!!dop_1_1_pr){ } else { dop_1_1_pr = 0; }
		if ( dop_1_1 == 1 ) { sum += dop_1_1_pr; }
		
		var dop_1_2 = $('#clt_dop_1_2:checked').val(); if (!!dop_1_2){ } else { dop_1_2 = 0; }
		var dop_1_2_pr = $('#clt_dop_1_2').data("price"); if (!!dop_1_2_pr){ } else { dop_1_2_pr = 0; }
		if ( dop_1_2 == 1 ) { sum += dop_1_2_pr; }
		
		var dop_1_3 = $('#clt_dop_1_3:checked').val(); if (!!dop_1_3){ } else { dop_1_3 = 0; }
		var dop_1_3_pr = $('#clt_dop_1_3').data("price"); if (!!dop_1_3_pr){ } else { dop_1_3_pr = 0; }
		if ( dop_1_3 == 1 ) { sum += dop_1_3_pr; }
		
		var dop_1_4 = $('#clt_dop_1_4:checked').val(); if (!!dop_1_4){ } else { dop_1_4 = 0; }
		var dop_1_4_pr = $('#clt_dop_1_4').data("price"); if (!!dop_1_4_pr){ } else { dop_1_4_pr = 0; }
		if ( dop_1_4 == 1 ) 
		{ 
			sum += dop_1_4_pr; 
			uvedomlenie = 1;
		}
		
		var dop_1_5 = $('#clt_dop_1_5:checked').val(); if (!!dop_1_5){ } else { dop_1_5 = 0; }
		var dop_1_5_pr = $('#clt_dop_1_5').data("price"); if (!!dop_1_5_pr){ } else { dop_1_5_pr = 0; }
		if ( dop_1_5 == 1 ) { sum += dop_1_5_pr; }

		var dop_1_6 = $('#clt_dop_1_6:checked').val(); if (!!dop_1_6){ } else { dop_1_6 = 0; }
		var dop_1_6_pr = $('#clt_dop_1_6').data("price"); if (!!dop_1_6_pr){ } else { dop_1_6_pr = 0; }
		if ( dop_1_6 == 1 ) { sum += dop_1_6_pr; }
		
	}
	
	if ( koleso_qq > 0 ) 
	{
		sum += koleso_pr * koleso_qq;
	}
		
	if ( vk == 2 ) 
	{
		var dop_2_1 = $('#clt_dop_2_1:checked').val(); if (!!dop_2_1){ } else { dop_2_1 = 0; }
		var dop_2_1_pr = $('#clt_dop_2_1').data("price"); if (!!dop_2_1_pr){ } else { dop_2_1_pr = 0; }
		if ( dop_2_1 == 1 ) { sum += dop_2_1_pr; }
		
		var dop_2_2 = $('#clt_dop_2_2:checked').val(); if (!!dop_2_2){ } else { dop_2_2 = 0; }
		var dop_2_2_pr = $('#clt_dop_2_2').data("price"); if (!!dop_2_2_pr){ } else { dop_2_2_pr = 0; }
		if ( dop_2_2 == 1 ) 
		{ 
			sum += dop_2_2_pr; 
			uvedomlenie = 1;
		}
		
		if ( koleso_qq > 0 ) 
		{
			uvedomlenie = 1;
		}
	}
	
	
	if ( skidka > 0 ) 
	{
		minus = ( sum * skidka / 100 );
		minus = Math.ceil( minus );
	}
	
	if ( ( predzakaz == 1 ) && ( sum > 0 ) )
	{
		minus += predzakaz_pr; 
	}
	
	
	$('.clt_old--js').addClass("d-none");


	if ( qq < 1 ) 
	{
		sum = 0;
	}
	else 
	{
		if ( minus > 0 ) 
		{
			old = sum;
			sum -= minus;
			
			old = old.toLocaleString();
			old += ' руб.' 
			
			$(".clt_old--js").text(old);
			$('.clt_old--js').removeClass("d-none");
		}
		
		if ( sum < 4000 ) 
		{
			sum = 4000;
		}
		
		sum = ( Math.ceil( sum /100 ) ) * 100;
		
		sum = sum.toLocaleString();
	
	}
		
	$(".clt_sum--js").text(sum);

}


function declOfNum(number, titles)  
{  
	cases = [2, 0, 1, 1, 1, 2];  
	return titles[ (number%100>4 && number%100<20)? 2 : cases[(number%10<5)?number%10:5] ];  
}


(function() {
  const phoneInputs = document.querySelectorAll('.phone-input');

  // Функция форматирования номера из введённых цифр.
  // Если цифр нет, возвращает "+7". Иначе добавляет пробел, скобки и разделители по шаблону.
  const formatNumber = (rawDigits) => {
	// Если ничего не введено, всегда показываем префикс
	if (rawDigits.length === 0) {
	  return "+7";
	}
	// Если строка не начинается с "7", добавляем её
	if (!rawDigits.startsWith('7')) {
	  rawDigits = '7' + rawDigits;
	}
	// Ограничиваем общее число цифр до 11 (одна для кода страны и 10 для номера)
	rawDigits = rawDigits.substring(0, 11);
	let output = "+7";
	const digitsAfter = rawDigits.substring(1); // цифры после первой "7"
	if (digitsAfter.length > 0) {
	  output += " (";
	  const areaCode = digitsAfter.substring(0, 3);
	  output += areaCode;
	  // Если введено 3 цифры кода, закрываем скобку
	  if (areaCode.length === 3) {
		output += ")";
	  }
	  const rest = digitsAfter.substring(3);
	  if (rest.length > 0) {
		output += " ";
		const p2 = rest.substring(0, 3);
		output += p2;
		const p3 = rest.substring(3, 5);
		if (p3) {
		  output += "-" + p3;
		}
		const p4 = rest.substring(5, 7);
		if (p4) {
		  output += "-" + p4;
		}
	  }
	}
	return output;
  };

  // Обработчик ввода: извлекает только цифры из поля и форматирует их
  const handleInput = (input) => {
	let cleanValue = input.value.replace(/\D/g, '');
	input.value = formatNumber(cleanValue);
  };

  // Обработчик вставки: очищает вставляемые данные и форматирует их
  const handlePaste = (input, e) => {
	e.preventDefault();
	let pasteData = (e.clipboardData || window.clipboardData).getData('text');
	let cleanPaste = pasteData.replace(/\D/g, '');
	// Если номер начинается с "8", заменяем её на "7",
	// если не начинается с "7" – добавляем её
	if (cleanPaste.startsWith('8')) {
	  cleanPaste = '7' + cleanPaste.substring(1);
	} else if (!cleanPaste.startsWith('7')) {
	  cleanPaste = '7' + cleanPaste;
	}
	input.value = formatNumber(cleanPaste);
	setTimeout(() => {
	  input.setSelectionRange(input.value.length, input.value.length);
	}, 0);
  };

  phoneInputs.forEach((input) => {
	// При загрузке, если поле пустое, устанавливаем значение по умолчанию "+7"
	if (!input.value) {
	  input.value = "+7";
	}

	input.addEventListener('focus', () => {
	  // Если по какой-то причине значение не начинается с "+7", вставляем его
	  if (!input.value.startsWith("+7")) {
		input.value = "+7";
	  }
	  setTimeout(() => {
		input.setSelectionRange(input.value.length, input.value.length);
	  }, 0);
	});

	input.addEventListener('input', () => handleInput(input));
	input.addEventListener('paste', (e) => handlePaste(input, e));

	// При потере фокуса, если после удаления цифр остается пустое поле или только "7",
	// возвращаем префикс "+7"
	input.addEventListener('blur', () => {
	  let cleanValue = input.value.replace(/\D/g, '');
	  if (cleanValue === "" || cleanValue === "7") {
		input.value = "+7";
	  }
	});
  });
  

})();

;(function($){
	'use strict';

		// Cookie
		var cookie = getCookie("cookie_read");
		
		if ( cookie == undefined || cookie != 1 ) 
		{
			setTimeout(function() { 
				$(".cookie_div--js").removeClass("d-none");
			}, 5000 )
		}
		
		$(document).on('click', '.cookie_btn--js', function(e){ 	
			e.preventDefault();

			writeCookie("cookie_read", 1, 30);
			$(".cookie_div--js").fadeOut();
		});	
		
		
		
	// Scrolls
	$(document).scroll(function () {
		
		var s_top = $(this).scrollTop();
		var page_w = $(window).width();
		
		if ( page_w > 991 )
		{
			if ( s_top > 90 ) 
			{
				$(".wx_header").addClass("wx_header_scroll");
				$('.wx_header_padd').css('display', 'none');
			}
			else 
			{
				$(".wx_header").removeClass("wx_header_scroll");
				$('.wx_header_padd').css('display', 'block');			
			}			
		}
	});
		
		
	// Mobile menu	
	$(document).on('click tap vclick', '.wx_mobile_hamburger--js', function(e){ 	
		e.preventDefault();
		
		if ($(this).hasClass("is-active")) 
		{
			$(this).removeClass("is-active");
			$('.wx_mobile_menu--js').addClass("d-none");
			$("main").css("display","block");
			$(".hide_whis_main--js").removeClass("d-none");			
		}
		else {
			$(this).addClass("is-active");
			$('.wx_mobile_menu--js').removeClass("d-none");
			$("main").css("display","none");
			$(".hide_whis_main--js").addClass("d-none");
		}
	});


	
	

	// Calculator v2
	$(document).on('click', '.clt_vk--js', function(e){ 
		e.preventDefault();

		// cur
		$(".clt_vk--js").removeClass("g-brd-primary g-bg-primary g-color-white");
		$(".clt_vk--js").addClass("g-brd-gray-light-v3 g-bg-white g-color-black");
		$(this).removeClass("g-brd-gray-light-v3 g-bg-white g-color-black");
		$(this).addClass("g-brd-primary g-bg-primary g-color-white");
	
		$(".clt_km--js").val(""); 
		$("#f_mesto").val(""); 
		$("#f_end").val(""); 
		

		var vk = $(this).data("vk"); if (!!vk){ } else { vk = 0; }
		if ( vk == 1 ) 
		{
			$(".clt_div_1--js").removeClass("d-none");
			$(".clt_div_2--js").addClass("d-none");
		}
		if ( vk == 2 ) 
		{
			$(".clt_div_2--js").removeClass("d-none");
			$(".clt_div_1--js").addClass("d-none");
		}
		
		$("#clt_vk").val(vk); 
		$(".clt_sum--js").text(0);
		
		SumRez ();
	});	


	// Calculator v2 - KM
	$(document).on('change keyup input', '.clt_km--js', function(e){ 
		e.preventDefault();

		var qq = $(this).val().replace(/[^0-9]/g, '');
		if ( qq > 99999 ) { qq = 99999; }
		
		this.value = qq;
	
		SumRez ();
	});
		
		
	// Calculator v2 change
	$(document).on('change', '.clt_smena--js', function(e){ 
		e.preventDefault();
		
		SumRez ();
	});	
	
	// Calculator v2 future
	$(document).on('change', '.clt_future--js', function(e){ 
		e.preventDefault();
	
		var predzakaz = $('#clt_predzakaz:checked').val(); if (!!predzakaz){ } else { predzakaz = 0; }	
		
		if ( predzakaz == 1 ) 
		{
			$(".clt_future_div--js").removeClass("d-none");	
		}
		else 
		{
			$(".clt_future_div--js").addClass("d-none");
		}
		
		SumRez ();
	});	
	

	// Calculator v2 dphone
	$(document).on('change', '.clt_dphone--js', function(e){ 
		e.preventDefault();
	
		var dphone = $('#clt_dphone:checked').val(); if (!!dphone){ } else { dphone = 0; }	
		
		if ( dphone == 1 ) 
		{
			$(".clt_dphone_div--js").removeClass("d-none");	
		}
		else 
		{
			$(".clt_dphone_div--js").addClass("d-none");
		}
	});	

	
	// Calculator v2 - Promo click
	$(document).on('click', '.clc_promo--js', function(e){ 
		e.preventDefault();

		$(this).addClass("d-none");
		$(".clc_promo_div--js").removeClass("d-none");	
	});	
	
	
	// Calculator v2 - Promo
	$(document).on('click', '.promo--js', function(e){ 
		e.preventDefault();
		
		var promo = $('#clt_promo').val(); if (!!promo){ } else { promo = ''; }
		
		if ( promo.length > 5 )
		{
			$.ajax({
				type: "GET",
				url: "/mod/_ajax/promo.php?promo=" + promo, 
				cache: false,
				success: function( skidka )
				{
					$("#clt_pskidka").val(skidka); 

					if ( skidka > 0 ) 
					{
						$(".promo_okey--js").removeClass("d-none");
						$(".promo_net--js").addClass("d-none");
					}
					else 
					{
						$(".promo_okey--js").addClass("d-none");
						$(".promo_net--js").removeClass("d-none");
					}
					
					SumRez ();
				}
			});	

		}
		
	});	
	
	
	// Calculator v2 - Form
	$("form.clt_form").submit(function(e){
        e.preventDefault();
	
		var forma       = $(this);
		var g_recaptcha = document.getElementById("g_recaptcha_response").value;
		
		$.ajax({
			type: "GET",
			url: "/mod/calculator.php?g_recaptcha="+g_recaptcha, 
			data: $(this).serialize(),
			cache: false,
			success: function(html)
			{
				forma.closest(".clt_form--js").html(html);	

				$("html, body").animate({ scrollTop: $( "#clc_form" ).offset().top - 100 }, 500); 				
			}
		});	
	
    });
	
	
	
	// Forms
	$("form.ajax_form").submit(function(e){
	    e.preventDefault();
	    var forma = $(this);
	    $.ajax({
	        type: "POST",
	        url: forma.attr("action"),
	        data: forma.serialize(),
	        headers: { "X-CSRFToken": getCookie("csrftoken") },
	        success: function(response) {
	            forma.closest(".ajax_form--js").html("<div class='alert alert-success'>Спасибо! Форма отправлена.</div>");
	        },
	        error: function() {
	            alert("Ошибка при отправке формы. Попробуйте ещё раз.");
	        }
	    });
	});

	

	$(document).on('click', '.question--js', function(e){ 	
		e.preventDefault();
	
		$(".ajax_name--js").html("Задать вопрос");
		
		$("#modal_backform").modal();
	});
	
	
	$("#modal_backform").on("hidden.bs.modal", function () {
		$(".ajax_name--js").html("Позвоните нам прямо сейчас");
	});


	$(document).on('click', '.bform_btn--js', function(e){ 	
		e.preventDefault();
	
		$(this).addClass("d-none");
		$(".bform--js").removeClass("d-none");
	});



	// WX popup
	var wx_popup_timeout = 0;
	$(document).on({
		mouseenter: function () 
		{			
			wx_popup_timeout = setTimeout(function() 
			{
				$(this).find(".wx_popup_div--js").css("display","block"); 
			}.bind(this), 100);
	
		},
		mouseleave: function () 
		{
			clearTimeout(wx_popup_timeout);
			$(this).find(".wx_popup_div--js").css("display","none");
		}
	}, ".wx_popup--js");
	

	// More - More
	$(document).on('click', '.more_more--js', function(e){ 	
		e.preventDefault();
	
		var name = $(this).data("name"); if (!!name){ } else { name = 'Показать все'; }	
		var name_2 = $(this).data("name_2"); if (!!name_2){ } else { name_2 = 'Скрыть'; }	

		if ($(this).hasClass("more_open"))
		{
			$(this).removeClass("more_open");
			$(this).closest(".more_parent--js").find(".more_one--js").addClass("d-none");
			$(this).html(name);
		}
		else 
		{
			$(this).addClass("more_open");	
			$(this).closest(".more_parent--js").find(".more_one--js").removeClass("d-none");
			$(this).html(name_2);
		}	
	});
	

	
	$(document).on("click", ".rating--js li", function(e){ 
		e.preventDefault();
		
		var rate_p = document.getElementById("rate_p").value;	
		var rate_d = document.getElementById("rate_d").value;	
		
		var star_star = $(this).data("val");


		$.ajax({
			url: "/mod/ajax_add_star.php?rate_p="+rate_p+"&rate_d="+rate_d+"&star_star="+star_star,
			cache: false,
			success: function( response ){
				
				if ( response[0] > 0 ) 
				{
					$(".rating_golos--js").removeClass("d-none");
					$(".rating_count--js").html( response[0] );
					$(".rating_star--js").html( response[1] );
					
					var okon = declOfNum( response[0],["оценка","оценки","оценок"]);	
					$(".rating_noun--js").html( okon );
					
					if ( star_star < 4 ) 
					{
						$(".ajax_name--js").html("Ваш голос учтён");
						$(".ajax_txt--js").html("Поделитесь причинами низкой оценки");
						$(".ajax_txt--js").removeClass("-color-black g-font-size-13");
						$(".ajax_txt--js").addClass("g-font-size-15 g-color-lightred");
						
						$("#modal_backform").modal();
					}
				}
			},
			dataType: "json"
		});
	
	});
		
		
	$(document).on("click", ".load_img_click--js", function(e){ 	
		e.preventDefault();
		
		var xx   = 0;
		var show = 2;

		if ( $(window).width() > 767 )
		{
			show = 4;
		}
		
		if ( $(window).width() > 991 )
		{
			show = 6;
		}
		
		$(".load_img--js").each(function(i, el) {	

			
			if ( $(el).hasClass("d-none"))
			{	
				++xx;
				
				if ( xx <= show )
				{
					$(el).removeClass("d-none");
				}
			}
	
		});	
		
		if ( xx < ( show + 1 ) ) 
		{
			$(".load_img_click--js").addClass("d-none");
		}
	});


	// Only digit
	$(document).on('change keyup input click', '.only_digit--js', function(e){ 
		e.preventDefault();
	
		var qq = $(this).val().replace(/[^0-9]/g, '');

		this.value = qq;
	});

		
})(jQuery);





$(document).ready(function () {

	$.HSCore.components.HSMaskedInput.init('[data-mask]');	

	$.HSCore.components.HSCarousel.init('[class*="js-carousel"]');
	$(".js-carousel").on('setPosition', function(event, slick) {
	  slick.$slider.css({
		opacity: 1,
		visibility: 'visible'
	  });
	});

	$('.wb_hidden_load_lg--js').removeClass("d-none");

	$.HSCore.components.HSGoTo.init('.js-go-to');
	
	$().fancybox({
		selector : '.slick-slide:not(.slick-cloned) a[data-fancybox]',
		hash : false
	});

	$.HSCore.helpers.HSRating.init();	
	
	$.HSCore.components.HSOnScrollAnimation.init('[data-animation]');
});