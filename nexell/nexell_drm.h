/*
 * Copyright (C) 2016  Nexell Co., Ltd.
 * Author: hyejung, kwon <cjscld15@nexell.co.kr>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sub license, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL
 * THE COPYRIGHT HOLDERS, AUTHORS AND/OR ITS SUPPLIERS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
 * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
 * USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * The above copyright notice and this permission notice (including the
 * next paragraph) shall be included in all copies or substantial portions
 * of the Software.
 *
 */

#ifndef _UAPI_NX_DRM_H_
#define _UAPI_NX_DRM_H_

#include <drm/drm.h>

/**
 * User-desired buffer creation information structure.
 *
 * @size: user-desired memory allocation size.
 *	- this size value would be page-aligned internally.
 * @flags: user request for setting memory type or cache attributes.
 * @handle: returned a handle to created gem object.
 *	- this handle will be set by gem module of kernel side.
 */
struct nx_drm_gem_create {
	uint64_t size;
	unsigned int flags;
	unsigned int handle;
	struct drm_gem_cma_object *obj;
};

/**
 * A structure to gem information.
 *
 * @handle: a handle to gem object created.
 * @flags: flag value including memory type and cache attribute and
 *	this value would be set by driver.
 * @size: size to memory region allocated by gem and this size would
 *	be set by driver.
 */
struct nx_drm_gem_info {
	unsigned int handle;
	unsigned int flags;
	uint64_t size;
};

#define DRM_NX_GEM_CREATE		0x00
/* Reserved 0x03 ~ 0x05 for nx specific gem ioctl */
#define DRM_NX_GEM_GET			0x04
//#define DRM_NX_VIDI_CONNECTION	0x07

#define DRM_IOCTL_NX_GEM_CREATE		DRM_IOWR(DRM_COMMAND_BASE + \
		DRM_NX_GEM_CREATE, struct nx_drm_gem_create)

#define DRM_IOCTL_NX_GEM_GET	DRM_IOWR(DRM_COMMAND_BASE + \
		DRM_NX_GEM_GET,	struct nx_drm_gem_info)

#endif
