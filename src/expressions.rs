use polars::prelude::{DataType::String, IntoSeries, PolarsResult, PolarsError::InvalidOperation, Series};
use pyo3_polars::derive::polars_expr;
use std::path::Path;

use polars_core::datatypes::{BooleanChunked, StringChunked};

#[polars_expr(output_type=Boolean)]
fn exists(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	String => {
	    let chunked_array = s.str()?;
	    let out: BooleanChunked = chunked_array.apply_generic(
		|value: Option<&str>| -> Option<bool> {
		    value.map(|s| Path::new(s).exists())
		}	
	    );
	    Ok(out.into_series())
	}
	_ => Err(InvalidOperation(format!("'exists' only works on string data, instead got {}", s.dtype()).into()))
    }
}

#[polars_expr(output_type=Boolean)]
fn is_absolute(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	String => {
	    let chunked_array = s.str()?;
	    let out: BooleanChunked = chunked_array.apply_generic(
		|value: Option<&str>| -> Option<bool> {
		    value.map(|s| Path::new(s).is_absolute())
		}
	    );
	    Ok(out.into_series())
	}
	_ => Err(InvalidOperation(format!("'is_absolute' only works on string data, instead got {}", s.dtype()).into()))
    }
}

#[polars_expr(output_type=Boolean)]
fn is_dir(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	String => {
	    let chunked_array = s.str()?;
	    let out: BooleanChunked = chunked_array.apply_generic(
		|value: Option<&str>| -> Option<bool> {
		    value.map(|s| Path::new(s).is_dir())
		}
	    );
	    Ok(out.into_series())
	}
	_ => Err(InvalidOperation(format!("'is_dir' only works on string data, instead got {}", s.dtype()).into()))
    }
}

#[polars_expr(output_type=Boolean)]
fn is_file(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	String => {
	    let chunked_array = s.str()?;
	    let out: BooleanChunked = chunked_array.apply_generic(
		|value: Option<&str>| -> Option<bool> {
		    value.map(|s| Path::new(s).is_file())
		}
	    );
	    Ok(out.into_series())
	}
	_ => Err(InvalidOperation(format!("'is_file' only works on string data, instead got {}", s.dtype()).into()))
    }
}

#[polars_expr(output_type=String)]
fn name(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	String => {
	    let chunked_array = s.str()?;
	    let out: StringChunked = chunked_array.apply_generic(
		|value: Option<&str>| -> Option<&str> {
		    value.map(
			|s| {
			    Path::new(s).file_name()
				.expect("a path ought to have a parent")
				.to_str()
				.expect("a path's parent ought to be able to be converted to a string")
		    }
		    )
		}
	    );
	    Ok(out.into_series())
	}
	_ => Err(InvalidOperation(format!("'name' only works on string data, instead got {}", s.dtype()).into()))
    }
}


#[polars_expr(output_type=String)]
fn parent(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	String => {
	    let chunked_array = s.str()?;
	    let out: StringChunked = chunked_array.apply_generic(
		|value: Option<&str>| -> Option<&str> {
		    value.map(
			|s| {
			    Path::new(s).parent()
				.expect("a path ought to have a parent")
				.to_str()
				.expect("a path ought to be able to be converted to a string")
			}
		    )
		}
	    );
	    Ok(out.into_series())
	}
	_ => Err(InvalidOperation(format!("'parent' only works on string data, instead got {}", s.dtype()).into()))
    }
}

