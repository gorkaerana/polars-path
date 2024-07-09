use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use std::path::Path;

use polars_core::datatypes::{BooleanChunked, StringChunked};

#[polars_expr(output_type=Boolean)]
fn exists(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	DataType::String => {
	    let ca = s.str()?;
	    let out: BooleanChunked = ca.apply_generic(
		|value: Option<&str>| -> Option<bool> {
		    Some(value.map_or(false, |s| Path::new(s).exists()))
		}
	    );
	    Ok(out.into_series())
	}
	_ => Err(PolarsError::InvalidOperation("exists only works on string data".into()))
    }
}

#[polars_expr(output_type=Boolean)]
fn is_absolute(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	DataType::String => {
	    let ca = s.str()?;
	    let out: BooleanChunked = ca.apply_generic(
		|value: Option<&str>| -> Option<bool> {
		    Some(value.map_or(false, |s| Path::new(s).is_absolute()))
		}
	    );
	    Ok(out.into_series())
	}
	_ => Err(PolarsError::InvalidOperation("is_absolute only works on string data".into()))
    }
}

#[polars_expr(output_type=Boolean)]
fn is_dir(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	DataType::String => {
	    let ca = s.str()?;
	    let out: BooleanChunked = ca.apply_generic(
		|value: Option<&str>| -> Option<bool> {
		    Some(value.map_or(false, |s| Path::new(s).is_dir()))
		}
	    );
	    Ok(out.into_series())
	}
	_ => Err(PolarsError::InvalidOperation("is_dir only works on string data".into()))
    }
}

#[polars_expr(output_type=Boolean)]
fn is_file(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	DataType::String => {
	    let ca = s.str()?;
	    let out: BooleanChunked = ca.apply_generic(
		|value: Option<&str>| -> Option<bool> {
		    Some(value.map_or(false, |s| Path::new(s).is_file()))
		}
	    );
	    Ok(out.into_series())
	}
	_ => Err(PolarsError::InvalidOperation("is_file only works on string data".into()))
    }
}

#[polars_expr(output_type=String)]
fn parent(inputs: &[Series]) -> PolarsResult<Series>{
    let s = inputs.get(0).expect("no series received");
    match s.dtype() {
	DataType::String => {
	    let ca = s.str()?;
	    let out: StringChunked = ca.apply_generic(
		|value: Option<&str>| -> Option<&str> {
		    Some(value.map_or("", |s| {
			Path::new(s).parent()
			    .expect("a path ought to have a parent")
			    .to_str()
			    .expect("a path ought to be able to be converted to a string")
		    }
		    )
		    )
		}
	    );
	    Ok(out.into_series())
	}
	_ => Err(PolarsError::InvalidOperation("parent only works on string data".into()))
    }
}
