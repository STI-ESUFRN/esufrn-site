// $(document).ready(function () {
//   $( "a:contains('Trajetória')").attr("href", "instituicao.historia.html")
//   $( "a:contains('Equipes')").attr("href", "instituicao.equipe.html")
//   $( "a:contains('Contato')").attr("href", "instituicao.contato.html")
//   $( "a:contains('Técnico')").attr("href", "ensino.tecnico.html")
//   $( "a:contains('Graduação')").attr("href", "ensino.graduacao.html")
//   $( "a:contains('Especialização')").attr("href", "ensino.especializacao.html")
//   $( "a:contains('Mestrado')").attr("href", "https://sigaa.ufrn.br/sigaa/public/programa/portal.jsf?lc=pt_BR&id=10489")
//   $( "a:contains('Pronatec')").attr("href", "ensino.pronatec.html")
//   $( "a:contains('Pesquisa')").attr("href", "")
//   $( "a:contains('Serviços')").attr("href", "biblioteca.servicos.html")
//   $( "a:contains('Manual')").attr("href", "biblioteca.manual.html")
//   $( "a:contains('Catálogo')").attr("href", "biblioteca.catalogo.html")
//   $( "a:contains('Chamado')").attr("href", "")
//   $( "a:contains('Reservas')").attr("href", "informatica.reserva.html")
//   $( "a:contains('Facebook')").attr("href", "")
//   $( "a:contains('Webmail')").attr("href", "")
//   $( "a:contains('Concursos Abertos')").attr("href", "")
//   $( "a:contains('oncursos Finalizados')").attr("href", "")
//   $( "a:contains('Processos Abertos')").attr("href", "")
//   $( "a:contains('Processos Finalizados')").attr("href", "")
// });
var altoContrate = false
$("#contraste").click(function (e) {
	e.preventDefault();

	// $("footer").css("background-color", "black");
	// $("section").css("background-color", "black");
	// $("body").css("background-color", "black");
	// $("h1").css("color", "white");
	// $("h1").css("color", "white");
	// $("#eventos").css("background-color", "black");
	// $(".btn-outline-dark").css("color", "black");
	// $(".btn-outline-dark").css("border-color", "black");
	// $("path").css("fill", "white");
	// $(".background-home").css("background-color", "black");
	// $(".text-white").css("background-color", "black");
	// $("#logo button").css("background-color", "black");
	// $(".news-item span").css("border", "5px solid white");
	if (altoContrate) {
		$("footer").removeClass("alto-contraste-bg");
		$(".navbar").removeClass("alto-contraste-bg");
		$("section").removeClass("alto-contraste-bg");
		$("body, .breadcrumb, .list-group-item").removeClass("alto-contraste-bg");
		$("a").removeClass("alto-contraste-bg");
		$(".dropdown-menu").removeClass("alto-contraste-bo");
		$("h1, h2, h3 ,h4, h5, .historia, .breadcrumb-item, a, li, p, b, label").removeClass("alto-contraste-cy");
		$("table").removeClass("alto-contraste-cy");
		$("#eventos").removeClass("alto-contraste-bg");
		$(".btn-outline-dark").removeClass("alto-contraste-cy");
		$(".btn-outline-dark").removeClass("alto-contraste-bc");
		$("path").removeClass("alto-contraste-fi");
		$(".background-home").removeClass("alto-contraste-bg");
		$(".text-white").removeClass("alto-contraste-bg").removeClass("alto-contraste-cy");
		$("#logo button").removeClass("alto-contraste-bg").removeClass("alto-contraste-cy");
		$(".news-item span").removeClass("alto-contraste-bo").removeClass("alto-contraste-cy");
		$(".btn-cursos .btn-primary").removeClass("alto-contraste-cy").removeClass("alto-contraste-bg");
		$(".depoimento-shadow span").removeClass("alto-contraste-sh");
		$(".menu-box").removeClass("alto-contraste-bg");
		$(".slide-owl").removeClass("alto-contraste-bc");
		$("#nav-box").removeClass("alto-contraste-bg-grad");
		$(".menu-container img").attr("src", "/static/assets/images/logotipo_ufrn_esufrn.low.png");
		altoContrate = false
	} else {
		$("footer").addClass("alto-contraste-bg");
		$(".navbar").addClass("alto-contraste-bg");
		$("section").addClass("alto-contraste-bg");
		$("body, .breadcrumb, .list-group-item").addClass("alto-contraste-bg");
		$("a").addClass("alto-contraste-bg");
		$(".dropdown-menu").addClass("alto-contraste-bo");
		$("h1, h2, h3 ,h4, h5, .historia, .breadcrumb-item, a, li, p, b, label").addClass("alto-contraste-cy");
		$("table").addClass("alto-contraste-cy");
		$("#eventos").addClass("alto-contraste-bg");
		$(".btn-outline-dark").addClass("alto-contraste-cy");
		$(".btn-outline-dark").addClass("alto-contraste-bc");
		$("path").addClass("alto-contraste-fi");
		$(".background-home").addClass("alto-contraste-bg");
		$(".text-white").addClass("alto-contraste-bg").addClass("alto-contraste-cy");
		$("#logo button").addClass("alto-contraste-bg").addClass("alto-contraste-cy");
		$(".news-item span").addClass("alto-contraste-bo").addClass("alto-contraste-cy");
		$(".btn-cursos .btn-primary").addClass("alto-contraste-cy").addClass("alto-contraste-bg");
		$(".depoimento-shadow span").addClass("alto-contraste-sh");
		$(".menu-box").addClass("alto-contraste-bg");
		$(".slide-owl").addClass("alto-contraste-bc");
		$("#nav-box").addClass("alto-contraste-bg-grad");
		$(".menu-container img").attr("src", "/static/assets/images/logotipo_ufrn_esufrn.low.png");
		altoContrate = true
	}
});
$("#form-contato [name]").change(function () {
	$(this).removeClass("is-invalid");
});
$("#enviar-mensagem").click(function (e) {
	e.preventDefault();

	$("#message-status-message").html("");
	$("#form-reserva input").removeClass("is-invalid");

	error = false;
	form_name = $("#form-contato [name=nome]");
	error += validate(form_name, form_name.val());

	form_contato = $("#form-contato [name=contato]");
	error += validate(form_contato, form_contato.val() && form_contato.val().isEmail());

	form_mensagem = $("#form-contato [name=mensagem]");
	error += validate(form_mensagem, form_mensagem.val());

	if (!error) {
		let serialized_data = $("#form-contato").serialize();
		$.ajax({
			type: "POST",
			url: "/api/contato/",
			data: serialized_data,
			success: function (response) {
				if (response.status == "success") {
					$("#message-status-message").text(response.message);
					$("#form-contato").trigger("reset");
				} else {
					$("#message-status-message").text(response.message);
				}
			}
		});
	}
	else {
		$("#message-status-message").text("Corrija os erros");
	}
});
