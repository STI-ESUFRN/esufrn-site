class ReservationCalendar {
	_defaultValues() {
		this.element = "reservation-calendar";
		this.weekName = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"];
		this.dayName = "Dia";
		this.daySeparator = [
			{
				id: "M",
				name: "Manhã"
			},
			{
				id: "T",
				name: "Tarde"
			},
			{
				id: "N",
				name: "Noite"
			}
		];
		this.varNames = {
			date: "date",
			event: "event",
			status: {
				name: "status",
				confirmed: "C",
				refused: "R",
				waiting: "W"
			},
			shift: "shift"
		};
		this.today = new Date();
	}

	_overwriteValues(data) {
		if (typeof (data) == "object") {
			$.each(data, (index, value) => {
				this[index] = value
			});
		} else {
			throw new Error("Missing object parameters!");
		}
	}

	constructor(data = false) {
		this._defaultValues();
		data ? this._overwriteValues(data) : NaN;

		this._createStruct();
	}

	_addColToStruct(id) {
		let auxString = "";
		this.daySeparator.forEach(element => {
			auxString += `
				<tr data-parent="${id}" data-turno="${element.id}">
				<th class="linha-turno" scope="row">${element.name}</th>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				</tr>
			`;
		});
		return auxString;
	}

	_addModal(){
		return `
		<div class="modal fade" id="reservation-details-modal" tabindex="-1" style="text-align: left!important;" role="dialog" aria-labelledby="reservation-details-label" aria-hidden="true">
		<div class="modal-dialog" role="document">
		  <div class="modal-content">
			<div class="modal-header">
			  <h5 class="modal-title" id="reservation-details-label">Detalhes da reserva</h5>
			  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
				<span aria-hidden="true">&times;</span>
			  </button>
			</div>
			<div class="modal-body">
			  ...
			</div>
			<div class="modal-footer">
			  <button type="button" class="btn btn-secondary" data-dismiss="modal">Fechar</button>
			</div>
		  </div>
		</div>
	  </div>`;
	}

	_addWeekRow(id) {
		return `
			<tr data-parent="${id}" class="tr-dia">
				<th id="semana-${id}" class="linha-dia" scope="row">${this.dayName}</th>
				<td data-sem="1"></td>
				<td data-sem="2"></td>
				<td data-sem="3"></td>
				<td data-sem="4"></td>
				<td data-sem="5"></td>
			</tr>
			${this._addColToStruct(id)}
			<tr class="table-separador" data-separador="${id}">
				<td colspan="100%"></td>
			</tr>
    	`;
	}

	_createStruct() {
		let template = `
			${this._addModal()}
			<div class="table-reserva d-flex justify-content-md-center">
				<div class="w-100">
					<table class="table reservation table-bordered text-center col-md-12 table-hover">
						<thead class="thead-light">
							<tr>
								<th scope="col"></th>
								<th scope="col">${this.weekName[1]}</th>
								<th scope="col">${this.weekName[2]}</th>
								<th scope="col">${this.weekName[3]}</th>
								<th scope="col">${this.weekName[4]}</th>
								<th scope="col">${this.weekName[5]}</th>
							</tr>
						</thead>
						<tbody>
							${this._addWeekRow(1)}
							${this._addWeekRow(2)}
							${this._addWeekRow(3)}
							${this._addWeekRow(4)}
							${this._addWeekRow(5)}
							${this._addWeekRow(6)}
						</tbody>
					</table>
				</div>
			</div>
		`;
		$(`#${this.element}`).html(template);
	}

	_generateCalendar(date) {
		this._createStruct();
		let numberDaysInMonth = date.daysInMonth();
		let weekNumberDayOne = date.day();
		// Ajustar para considerar apenas dias úteis (1-5: Segunda a Sexta)
		// Se o mês começa no domingo (0), ajustar para começar na segunda
		if (weekNumberDayOne === 0) {
			weekNumberDayOne = 7; // Domingo vira último dia
		}
		// Se o mês começa no sábado (6), ajustar para começar na segunda
		if (weekNumberDayOne === 6) {
			weekNumberDayOne = 7; // Sábado vira além da sexta
		}
		
		let trDia = $(`#${this.element} .tr-dia [data-sem]`)
		let currentDay = 1;

		$.each(trDia, (index, value) => {
			while (currentDay <= numberDaysInMonth) {
				let tempDate = moment(date).date(currentDay);
				let dayOfWeek = tempDate.day();
				
				// Pular fins de semana (0=domingo, 6=sábado)
				if (dayOfWeek === 0 || dayOfWeek === 6) {
					currentDay++;
					continue;
				}
				
				// Verificar se estamos na coluna correta (1-5 = segunda a sexta)
				if (parseInt($(value).attr('data-sem')) === dayOfWeek) {
					$(value).text(currentDay);
					$(value).attr('data-day', currentDay);
					currentDay++;
					break;
				} else {
					break;
				}
			}
			
			// Remover linhas extras vazias
			if (currentDay > numberDaysInMonth) {
				let dataParent = $(value).parent().attr("data-parent");
				let hasContent = false;
				$(`[data-parent="${dataParent}"] [data-sem]`).each(function() {
					if ($(this).text().trim() !== '') {
						hasContent = true;
						return false;
					}
				});
				
				if (!hasContent) {
					$(`[data-parent="${dataParent}"]`).remove();
					$(`[data-separador="${dataParent}"]`).remove();
					return false;
				}
			}
		});

		$('#reservation-details-modal').on('show.bs.modal', function (e) {
			let current_index = $(e.relatedTarget).attr("data-id");
			$.get(`/api/calendar/${current_index}/`, (response) =>{
				let modal_body = $(this).find(".modal-body");
				modal_body.html("");
				modal_body.append(
					$("<p />", {html: `<small>Evento:</small> <b>${response.event}</b>`}),
					$("<p />", {html: `<small>Solicitante:</small> <b>${response.requester}</b>`}),
				);
			});
		});
	}

	_updateReservations(data) {
		$.each(data, (index, value) => {
			try {
				let eventDate = moment(value[this.varNames.date]);
				let eventDay = eventDate.date();
				let eventWeekDay = eventDate.day();
				
				// Pular eventos em fins de semana
				if (eventWeekDay === 0 || eventWeekDay === 6) {
					return true; // continue
				}
				
				// Encontrar a célula correta baseada no dia do mês e dia da semana
				let targetCell = null;
				$(`#${this.element} .tr-dia [data-sem="${eventWeekDay}"]`).each(function() {
					if ($(this).text().trim() == eventDay) {
						targetCell = $(this);
						return false;
					}
				});
				
				if (!targetCell) {
					console.warn(`Could not find cell for day ${eventDay}, weekday ${eventWeekDay}`);
					return true;
				}
				
				let parentNumber = targetCell.parent().attr("data-parent");
				let arrayLine = $(`#${this.element} [data-parent='${parentNumber}'][data-turno='${value[this.varNames.shift]}'] td`);
				
				// Encontrar o índice correto na linha baseado no dia da semana (1-5)
				let columnIndex = eventWeekDay - 1; // Segunda=1 -> índice 0, etc.
				
				let indicatorBall = ""
				switch (value[this.varNames.status.name]) {
					case this.varNames.status.confirmed:
						indicatorBall = "y-confirmado"
						break;
					case this.varNames.status.refused:
						indicatorBall = "n-confirmado"
						break;
					case this.varNames.status.waiting:
						indicatorBall = "w-confirmado"
						break;
				}
				
				if (arrayLine[columnIndex]) {
					arrayLine[columnIndex].innerHTML += `<div class='w-100 h-100' data-toggle="modal" data-target="#reservation-details-modal" data-id=${value["id"]} title='${value[this.varNames.event]}'><i class="fas fa-circle ${indicatorBall}"></i> ${value[this.varNames.event]} </div>`
				}
			} catch (error) {
				console.warn(`Something went wrong when processing reservation:`, error, value);
			}
		});
	}

	updateCalendar(data, year, month) {
		let newdate = moment(`${year}-${month}`, "Y-M");
		this._generateCalendar(newdate);
		this._updateReservations(data);
	}
}

