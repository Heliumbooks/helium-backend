/**
 * filters.js
 * To preserve and restore filters per session.
 *
 * If filterForm is in the document, all fields will
 * be stored in the session when the user clicks the
 * filter button.
 *
 * When filtered is not in the querystring, but session
 * filters exist, the form elements will be populated
 * with the values from the session.
 *
 * @TODO: Make this usable for any page, not just reservations.
 *
 */

function preserveFilters() {

	/** Gets all the elements of a form, including the
	 * select and textarea elements.
 	 * @param element
	 * @returns {unknown[]}
	 */
	const getElements = element => Array.from(element.elements).filter(tag => ["select", "textarea", "input"].includes(tag.tagName.toLowerCase()));

    /**
	 * I am not using the URLSearchParams interface because it
	 * is not currently supported by Internet Explorer
	 *
	 * Get the URL parameters
	 * source: https://css-tricks.com/snippets/javascript/get-url-variables/
	 * @param  {String} url The URL
	 * @return {Object}     The URL parameters
	 */
	const getParams = function (url) {
		var params = {};
		var parser = document.createElement('a');
		parser.href = url;
		var query = parser.search.substring(1);
		var vars = query.split('&');
		for (var i = 0; i < vars.length; i++) {
			var pair = vars[i].split('=');
			params[pair[0]] = decodeURIComponent(pair[1]);
		}
		return params;
	};

	const form = document.getElementById('filterForm');
	if (form) {
		/* Setup an event listener to save all the fields to the
		   session when the user clicks the filter button.
		 */
		form.addEventListener('submit', function() {
			/** @TODO: If all filters are cleared, remove the filtered value, so that we don't reload when there aren't actually any filters. */
			getElements(form).forEach(function(el) {
				sessionStorage.setItem(el.id, el.value);
			});
			sessionStorage.setItem("filtered", "true");
		});
		/* If the user has come to this page without the filtered
		   parameter being set, then get the session values, if there
		   are any, and submit the filter
		 */
		const params = getParams(window.location.href);
		if (!("filtered" in params)) {
			/* Hide the results table and footer so the user
			   doesn't see them come and go while the filters
			   are applied
			 */
			const results_el = document.getElementById("results-body");
			if (results_el) { results_el.style.display = "none"; }
			const footer_el = document.getElementById("results-footer");
			if (footer_el) { footer_el.style.display = "none"; }

			if (sessionStorage.getItem("filtered") == "true") {
				getElements(form).forEach(function(el) {
					el.value = sessionStorage.getItem(el.id);
				});
				form.submit();
			}
		}
	}
}

document.addEventListener("DOMContentLoaded", () => { preserveFilters(); });