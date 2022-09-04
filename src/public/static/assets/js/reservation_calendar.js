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
				<td></td>
				<td></td>
				</tr>
			`;
		});
		return auxString;
	}

	_addWeekRow(id) {
		return `
			<tr data-parent="${id}" class="tr-dia">
				<th id="semana-${id}" class="linha-dia" scope="row">${this.dayName}</th>
				<td data-sem="0"></td>
				<td data-sem="1"></td>
				<td data-sem="2"></td>
				<td data-sem="3"></td>
				<td data-sem="4"></td>
				<td data-sem="5"></td>
				<td data-sem="6"></td>
			</tr>
			${this._addColToStruct(id)}
			<tr class="table-separador" data-separador="${id}">
				<td colspan="100%"></td>
			</tr>
    	`;
	}

	_createStruct() {
		let template = `
			<div class="table-reserva d-flex justify-content-md-center">
				<div class="w-100">
					<table class="table reservation table-bordered text-center col-md-12 table-hover">
						<thead class="thead-light">
							<tr>
								<th scope="col"></th>
								<th scope="col">${this.weekName[0]}</th>
								<th scope="col">${this.weekName[1]}</th>
								<th scope="col">${this.weekName[2]}</th>
								<th scope="col">${this.weekName[3]}</th>
								<th scope="col">${this.weekName[4]}</th>
								<th scope="col">${this.weekName[5]}</th>
								<th scope="col">${this.weekName[6]}</th>
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
		let trDia = $(`#${this.element} .tr-dia [data-sem]`)

		$.each(trDia, (index, value) => {
			if (index < weekNumberDayOne + numberDaysInMonth && weekNumberDayOne <= index) {
				trDia[index].innerText = index - weekNumberDayOne + 1;
			} else if (trDia[weekNumberDayOne + numberDaysInMonth - 1].parentElement.getAttribute("data-parent") < value.parentElement.getAttribute("data-parent")) {
				let dataParentExtra = value.parentElement.getAttribute("data-parent")
				$(`[data-parent = ${dataParentExtra}]`).remove()
				$(`[data-separador = ${dataParentExtra}]`).remove()
				return false;
			}
		});

	}

	_updateReservations(data) {
		$.each(data, (index, value) => {
			try {
				let eventDay = moment(value[this.varNames.date]).date();
				let eventWeekDay = $(`#${this.element} .tr-dia td:contains(${eventDay})`).attr("data-sem")
				let parentNumber = $(`#${this.element} .tr-dia td:contains(${eventDay})`).parent().attr("data-parent")
				let arrayLine = $(`#${this.element} [data-parent='${parentNumber}'][data-turno='${value[this.varNames.shift]}'] td`)
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
				arrayLine[eventWeekDay].innerHTML += `<div class='w-100 h-100' title='${value[this.varNames.event]}'><i class="fas fa-circle ${indicatorBall}"></i> ${value[this.varNames.event]} </div>`
			} catch {
				console.warn(`Something went wrong when field 'shift[${value.shift}]' was being filled! Check if this field was setted.`);
			}
		});
	}

	updateCalendar(data, year, month) {
		let newdate = moment(`${year}-${month}`, "Y-M");
		this._generateCalendar(newdate);
		this._updateReservations(data);
	}
}